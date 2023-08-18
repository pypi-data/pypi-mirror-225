import pytest
import json

from pytest import Parser, Session, Config, Item, CallInfo
from .connector import Connector
from .decorator_updater import update_tests
from .testRunConfig import TestRunConfig
from .testItem import TestItem
from .code_collector import get_functions_source_by_name
from .s3_connector import S3Connector
import logging

log = logging.getLogger('analyzer')
log.setLevel('INFO')

metadata_file = 'metadata.json'
decorator_name = 'testomatio'
analyzer_option = 'analyzer'

help_text = 'analize tests, connect test with testomat.io. Use parameters:\n' \
            'add - upload tests and set test ids in the code\n' \
            'remove - removes testomat.io ids from the ALL tests\n' \
            'sync - allows to share sync test run status with testomat.io\n' \
            'debug - saves analyzed test metadata to the json in the test project root\n'


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(f'--{analyzer_option}',
                     action='store',
                     help=help_text)
    parser.addoption(f'--testRunEnv',
                     action='store',
                     help='specify test run environment for testomat.io. Works only with --analyzer sync')

    parser.addini('testomatio_url', 'testomat.io base url', default='https://app.testomat.io')
    parser.addini('testomatio_project', 'testomat.io project api key')
    parser.addini('testomatio_email', 'testomat.io user email')
    parser.addini('testomatio_password', 'testomat.io user password')

    parser.addini('testomatio_s3_access_key_id', 's3 access key id to save artifacts', default=None)
    parser.addini('testomatio_s3_secret_key_id', 's3 secret key id to save artifacts', default=None)
    parser.addini('testomatio_s3_endpoint', 's3 endpoint', default=None)
    parser.addini('testomatio_s3_bucket', 's3 bucket name (optional)', default=None)


def pytest_configure(config: Config):
    config.addinivalue_line(
        "markers", "testomatio(arg): built in marker to connect test case with testomat.io by unique id"
    )

    pytest.analyzer_test_run_config = TestRunConfig()

    if config.getoption(analyzer_option):
        url = config.getini('testomatio_url')
        project = config.getini('testomatio_project')
        email = config.getini('testomatio_email')
        password = config.getini('testomatio_password')
        connector = Connector(email, password, url, project)
        connector.connect()
        pytest.connector = connector
        if config.getoption('testRunEnv'):
            pytest.analyzer_test_run_config.environment = config.getoption('testRunEnv')

    s3_access_key = config.getini('testomatio_s3_access_key_id')
    s3_secret_key = config.getini('testomatio_s3_secret_key_id')
    s3_endpoint = config.getini('testomatio_s3_endpoint')
    s3_bucket = config.getini('testomatio_s3_bucket')
    pytest.s3_connector = None
    if all((s3_access_key, s3_secret_key, s3_endpoint)):
        pytest.s3_connector = S3Connector(s3_access_key, s3_secret_key, s3_endpoint, s3_bucket)


def collect_tests(items: list[Item]):
    meta: list[TestItem] = list()
    test_files: set = set()
    test_names: list = list()
    parameter_filter: set[Item] = set()
    for item in items:
        if item.function not in parameter_filter:
            parameter_filter.add(item.function)
            ti = TestItem(item)
            test_files.add(ti.abs_path)
            test_names.append(ti.title)
            meta.append(ti)

    for test_file in test_files:
        pairs = [p for p in get_functions_source_by_name(test_file, test_names)]
        for ti in meta:
            for name, source_code in pairs:
                if ti.title == name and ti.abs_path == test_file:
                    ti.source_code = source_code
                    break
    return meta, test_files, test_names


def add_and_enrich_tests(meta: list[TestItem], test_files: set, test_names: list, connector: Connector):
    connector = pytest.connector
    connector.load_tests(meta)
    connector.enrich_test_with_ids(meta)
    connector.disconnect()
    mapping = get_test_mapping(meta)
    for test_file in test_files:
        update_tests(test_file, mapping, test_names, decorator_name)


def pytest_collection_modifyitems(session: Session, config: Config, items: list[Item]) -> None:
    if config.getoption(analyzer_option):
        meta, test_files, test_names = collect_tests(items)
        connector: Connector = pytest.connector
        match config.getoption(analyzer_option):
            case 'add':
                add_and_enrich_tests(meta, test_files, test_names, connector)
                pytest.exit(
                    f'{len(items)} found. {len(meta)} unique test functions data collected and updated.'
                    f'Exit without test execution')
            case 'remove':
                mapping = get_test_mapping(meta)
                for test_file in test_files:
                    update_tests(test_file, mapping, test_names, decorator_name, remove=True)
                pytest.exit(
                    f'{len(items)} found. tests ids removed. Exit without test execution')
            case 'sync':
                test_config = pytest.analyzer_test_run_config
                pytest.analyzer_test_run_config.test_run_id = connector.create_test_run(**test_config.to_dict())
            case 'debug':
                with open(metadata_file, 'w') as file:
                    data = json.dumps([i.to_dict() for i in meta], indent=4)
                    file.write(data)
                pytest.exit(
                    f'saved metadata to {metadata_file}. Exit without test execution')
            case _:
                pytest.exit('Unknown analyzer parameter. Use one of: add, remove, sync, debug')


def pytest_runtest_makereport(item: Item, call: CallInfo):
    sync = item.config.getoption(analyzer_option)
    if not sync:
        return
    elif not pytest.analyzer_test_run_config.test_run_id:
        return

    test_item = TestItem(item)
    request = {
        'status': None,
        'title': test_item.title,
        'run_time': call.duration,
        'suite_title': test_item.file_name,
        'suite_id': None,
        'test_id': test_item.id[2:] if test_item.id else None,  # remove @T if exists
        'message': None,
        'stack': None,
        'example': None,
        'artifacts': None,
        'steps': None,
        'code': None,
    }
    if call.when == 'setup':
        if call.excinfo is not None:
            if call.excinfo.typename == 'Skipped':
                request['status'] = 'skipped'
            else:
                request['message'] = str(call.excinfo.value)
                request['stack'] = '\n'.join((str(tb) for tb in call.excinfo.traceback))
                request['status'] = 'failed'
    if call.when == 'call':
        if call.excinfo is not None:
            request['message'] = str(call.excinfo.value)
            request['stack'] = '\n'.join((str(tb) for tb in call.excinfo.traceback))
            request['status'] = 'failed'
        else:
            request['status'] = 'passed'

    if request['status']:
        connector = pytest.connector
        request['artifacts'] = getattr(item, 'testomatio_artifacts', None)
        connector.update_test_status(run_id=pytest.analyzer_test_run_config.test_run_id, **request)


def pytest_sessionfinish(session: Session, exitstatus: int):
    if pytest.analyzer_test_run_config.test_run_id:
        connector = pytest.connector
        connector.finish_test_run(pytest.analyzer_test_run_config.test_run_id)


def add_decorators(files, mapping, tests):
    for test_file in files:
        update_tests(test_file, mapping, tests, decorator_name)


def get_test_mapping(tests: list[TestItem]) -> list[tuple[str, int]]:
    return [(test.title, test.id) for test in tests]
