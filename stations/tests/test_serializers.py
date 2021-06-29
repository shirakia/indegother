from django.test import TestCase
from stations.serializers import StationSerializer


class TestStationSerializer(TestCase):

    def setUp(self):
        self.data = {
            'kioskId': 3000,
            'at': '2019-09-01T10:00:00',
            'document': {'dummy': 'document'},
        }

    def test_validate(self):
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_validate_kioskId_exists(self):
        self.data.pop('kioskId')
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['kioskId'][0]), 'This field is required.')

    def test_validate_at_exists(self):
        self.data.pop('at')
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['at'][0]), 'This field is required.')

    def test_validate_kioskId_at_unique(self):
        serializer = StationSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['non_field_errors'][0]),
                         'The fields kioskId, at must make a unique set.')

    def test_validate_kioskId_at_unique_pass_with_different_kioskId(self):
        serializer = StationSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        self.data['kioskId'] = 3001
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_validate_kioskId_at_unique_pass_with_different_at(self):
        serializer = StationSerializer(data=self.data)
        serializer.is_valid()
        serializer.save()

        self.data['at'] = '2019-09-01T10:00:01'
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_invallid_at(self):
        self.data['at'] = 'invalid datetime string'
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(
            str(serializer.errors['at'][0]),
            'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].')  # noqa

    def test_invallid_kioskId(self):
        self.data['kioskId'] = '3000 in string'
        serializer = StationSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(str(serializer.errors['kioskId'][0]), 'A valid integer is required.')
