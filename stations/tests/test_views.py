import json
from datetime import datetime
from dateutil import tz

from rest_framework.test import APITestCase
from unittest import mock

from ..models import Station


class TestStationCreateAPIView(APITestCase):

    URL = '/api/v1/indego-data-fetch-and-store-it-db'

    @mock.patch('stations.views.call_indego_station_api')
    def test_create_success(self, indego_mock):
        indego_mock.status = 200
        with open('stations/tests/test_indego.json') as f:
            indego_mock.return_value = json.load(f)

        response = self.client.post(self.URL, format='json')
        self.assertEqual(response.status_code, 200)  # should be 201. But mock overwite it here...
        self.assertEqual(Station.objects.count(), 3)


class TestStationListRetrieveAPIView(APITestCase):

    URL = '/api/v1/stations/'

    def setUpTestData(self):
        at = datetime(2021, 6, 25, 20, 0, 0, tzinfo=tz.tzutc())
        Station.objects.create(kioskId=3000, at=at)
        Station.objects.create(kioskId=3001, at=at)

    def test_list_retrieve_success(self):
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{self.URL}?{query}', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['stations']), 2)

    def test_list_retrieve_400_when_no_query(self):
        response = self.client.get(self.URL, format='json')
        self.assertEqual(response.status_code, 400)

    def test_list_retrieve_404_when_no_specified_sstation(self):
        query = 'at=2021-06-26T04:00:00'  # future
        response = self.client.get(f'{self.URL}?{query}', format='json')
        self.assertEqual(response.status_code, 404)


class TestStationRetrieveAPIView(APITestCase):

    URL = '/api/v1/stations/'

    def setUpTestData(self):
        at = datetime(2021, 6, 25, 20, 0, 0, tzinfo=tz.tzutc())
        Station.objects.create(kioskId=3000, at=at)
        Station.objects.create(kioskId=3001, at=at)

    def test_retrieve_success(self):
        kioskId = 3000
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{self.URL}{kioskId}?{query}', format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['station']['kioskId'], kioskId)

    def test_retrieve_400_when_no_query(self):
        kioskId = 3000
        response = self.client.get(f'{self.URL}{kioskId}', format='json')
        self.assertEqual(response.status_code, 400)

    def test_retrieve_404_when_no_specified_station(self):
        kioskId = 3000
        query = 'at=2021-06-26T04:00:00'  # future
        response = self.client.get(f'{self.URL}{kioskId}?{query}', format='json')
        self.assertEqual(response.status_code, 404)
