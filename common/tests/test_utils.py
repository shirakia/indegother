import requests

from django.test import TestCase
from unittest import mock

from common import utils


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.raise_for_status = mock.Mock()

    def json(self):
        return self.json_data


class TestUtil(TestCase):
    @mock.patch.object(requests.Session, 'get')
    def test_call_external_api(self, get_mock):
        json_value = {'dummy': 'data'}
        get_mock.return_value = MockResponse(json_value, 200)
        self.assertEqual(utils.call_external_api(''), json_value)
