from django.test import TestCase
from weathers.serializers import WeatherSerializer


class TestWeatherSerializer(TestCase):

    def setUp(self):
        self.data = {
            'at': '2019-09-01T10:00:00',
            'document': {'dummy': 'document'},
        }

    def test_validate(self):
        serializer = WeatherSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_validate_at_exists(self):
        self.data.pop('at')
        serializer = WeatherSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['at'][0]), 'This field is required.')

    def test_validate_at_unique(self):
        serializer = WeatherSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        serializer = WeatherSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['at'][0]), 'This field must be unique.')

    def test_validate_at_unique_pass_with_different_at(self):
        serializer = WeatherSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        self.data['at'] = '2019-09-01T10:00:01'
        serializer = WeatherSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_invallid_at(self):
        self.data['at'] = 'invalid datetime string'
        serializer = WeatherSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(
            str(serializer.errors['at'][0]),
            'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].')  # noqa
