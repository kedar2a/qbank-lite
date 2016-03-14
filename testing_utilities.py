import os
import json
import shutil

from dlkit_edx.primordium import Type
from nose.tools import *
from paste.fixture import TestApp
from records.registry import LOG_ENTRY_RECORD_TYPES
from unittest import TestCase

from dlkit_edx import PROXY_SESSION, RUNTIME
from dlkit_edx.proxy_example import TestRequest
from dlkit_edx.utilities import impl_key_dict
import dlkit_edx.configs


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))
TEST_DATA_STORE = ABS_PATH + '/test_datastore'

TEXT_BLOB_RECORD_TYPE = Type(**LOG_ENTRY_RECORD_TYPES['text-blob'])

def configure_dlkit():
    dlkit_edx.configs.FILESYSTEM_1 = {
        'id': 'filesystem_configuration_1',
        'displayName': 'Filesystem Configuration',
        'description': 'Configuration for Filesystem Implementation',
        'parameters': {
            'implKey': impl_key_dict('filesystem'),
            'dataStorePath': {
                'syntax': 'STRING',
                'displayName': 'Path to local filesystem datastore',
                'description': 'Filesystem path for setting the MongoClient host.',
                'values': [
                    {'value': TEST_DATA_STORE, 'priority': 1}
                ]
            },
            'recordsRegistry': {
                'syntax': 'STRING',
                'displayName': 'Python path to the extension records registry file',
                'description': 'dot-separated path to the extension records registry file',
                'values': [
                    {'value': 'records.registry', 'priority': 1}
                ]
            },
        }
    }

configure_dlkit()

from main import app


def create_test_bank():
    am = get_managers()['am']
    form = am.get_bank_form_for_create([])
    form.display_name = 'an assessment bank'
    form.description = 'for testing with'
    return am.create_bank(form)

def get_managers():
    managers = [('am', 'ASSESSMENT'),
                ('logm', 'LOGGING')]
    results = {}
    for manager in managers:
        nickname = manager[0]
        service_name = manager[1]
        condition = PROXY_SESSION.get_proxy_condition()
        dummy_request = TestRequest(username='student@tiss.edu', authenticated=True)
        condition.set_http_request(dummy_request)
        proxy = PROXY_SESSION.get_proxy(condition)
        results[nickname] = RUNTIME.get_service_manager(service_name,
                                                        proxy=proxy)
    return results


class BaseTestCase(TestCase):
    """
    """
    def code(self, _req, _code):
        self.assertEqual(_req.status, _code)

    def create_new_log(self):
        logm = get_managers()['logm']
        form = logm.get_log_form_for_create([])
        form.display_name = 'my new log'
        form.description = 'for testing with'
        return logm.create_log(form)

    def created(self, _req):
        self.code(_req, 201)

    def deleted(self, _req):
        self.code(_req, 202)

    def json(self, _req):
        return json.loads(_req.body)

    def message(self, _req, _msg):
        self.assertIn(_msg, str(_req.body))

    def ok(self, _req):
        self.assertEqual(_req.status, 200)

    def setUp(self):
        configure_dlkit()
        middleware = []
        self.app = TestApp(app.wsgifunc(*middleware))

        if not os.path.isdir(TEST_DATA_STORE):
            os.makedirs(TEST_DATA_STORE)
        shutil.rmtree(TEST_DATA_STORE)

    def setup_entry(self, log_id, data):
        logm = get_managers()['logm']

        log = logm.get_log(log_id)

        form = log.get_log_entry_form_for_create([TEXT_BLOB_RECORD_TYPE])
        form.set_text(data)

        new_entry = log.create_log_entry(form)

        return new_entry

    def tearDown(self):
        shutil.rmtree(TEST_DATA_STORE)