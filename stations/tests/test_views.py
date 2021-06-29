import json
from datetime import datetime
from dateutil import tz

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from unittest import mock


from ..models import Station
from weathers.models import Weather


def create_token() -> str:
    user = User.objects.create_user('test', 'test@example.com', 'password')
    return Token.objects.create(user=user).key


class TestStationCreateAPIView(APITestCase):

    URL = '/api/v1/indego-data-fetch-and-store-it-db'

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + create_token())

    @mock.patch('stations.views.call_openweathermap_api')
    @mock.patch('stations.views.call_indego_station_api')
    def test_create_success(self, indego_mock, weather_mock):
        indego_mock.status = 200
        with open('stations/tests/test_indego.json') as f:
            indego_mock.return_value = json.load(f)
        weather_mock.status = 200
        with open('stations/tests/test_weather.json') as f:
            weather_mock.return_value = json.load(f)

        response = self.client.post(self.URL, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Station.objects.count(), 3)
        self.assertEqual(Weather.objects.count(), 1)


class TestStationListRetrieveAPIView(APITestCase):

    URL = '/api/v1/stations/'

    @classmethod
    def setUpTestData(cls):
        at = datetime(2021, 6, 25, 20, 0, 0, tzinfo=tz.tzutc())
        Station.objects.create(kioskId=3000, at=at, document={'dummy': 'document'})
        Station.objects.create(kioskId=3001, at=at, document={'dummy': 'document'})
        Weather.objects.create(at=at, document={'dummy': 'document'})

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + create_token())

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


class TestStationListRetrieveAPIViewWhenNoWeather(APITestCase):

    URL = '/api/v1/stations/'

    @classmethod
    def setUpTestData(cls):
        at = datetime(2021, 6, 25, 20, 0, 0, tzinfo=tz.tzutc())
        Station.objects.create(kioskId=3000, at=at, document={'dummy': 'document'})
        Station.objects.create(kioskId=3001, at=at, document={'dummy': 'document'})

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + create_token())

    def test_list_retrieve_404(self):
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{self.URL}?{query}', format='json')
        self.assertEqual(response.status_code, 404)


class TestStationRetrieveAPIView(APITestCase):

    URL = '/api/v1/stations/'

    @classmethod
    def setUpTestData(cls):
        at = datetime(2021, 6, 25, 20, 0, 0, tzinfo=tz.tzutc())
        Station.objects.create(kioskId=3000, at=at, document={'dummy': 'document'})
        Station.objects.create(kioskId=3001, at=at, document={'dummy': 'document'})
        Weather.objects.create(at=at, document={'dummy': 'document'})

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + create_token())

    def test_retrieve_success(self):
        kioskId = 3000
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{self.URL}{kioskId}?{query}', format='json')

        self.assertEqual(response.status_code, 200)

    def test_retrieve_400_when_no_query(self):
        kioskId = 3000
        response = self.client.get(f'{self.URL}{kioskId}', format='json')
        self.assertEqual(response.status_code, 400)

    def test_retrieve_404_when_no_specified_station(self):
        kioskId = 3000
        query = 'at=2021-06-26T04:00:00'  # future
        response = self.client.get(f'{self.URL}{kioskId}?{query}', format='json')
        self.assertEqual(response.status_code, 404)


class TestStationRetrieveAPIViewWhenNoWeather(APITestCase):

    URL = '/api/v1/stations/'

    @classmethod
    def setUpTestData(cls):
        at = datetime(2021, 6, 25, 20, 0, 0, tzinfo=tz.tzutc())
        Station.objects.create(kioskId=3000, at=at, document={'dummy': 'document'})
        Station.objects.create(kioskId=3001, at=at, document={'dummy': 'document'})

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + create_token())

    def test_retrieve_404(self):
        kioskId = 3000
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{self.URL}{kioskId}?{query}', format='json')

        self.assertEqual(response.status_code, 404)


class TestWithoutToken(APITestCase):

    def test_create_401(self):
        url = '/api/v1/indego-data-fetch-and-store-it-db'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 401)

    def test_stations_list_retreice_401(self):
        url = '/api/v1/stations/'
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{url}?{query}', format='json')
        self.assertEqual(response.status_code, 401)

    def test_stations_retreice_401(self):
        url = '/api/v1/stations/'
        kioskId = 3000
        query = 'at=2021-06-25T04:00:00'
        response = self.client.get(f'{url}{kioskId}?{query}', format='json')
        self.assertEqual(response.status_code, 401)
