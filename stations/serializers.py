from rest_framework import serializers, validators

from .models import Station


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        exclude = ['uuid']
        extra_kwargs = {
            'kioskId': {'write_only': True},
            'at': {'write_only': True},
        }
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Station.objects.all(),
                fields=['kioskId', 'at']
            )
        ]

    document = serializers.DictField()

    def to_representation(self, instance):
        return super().to_representation(instance)['document']


class StationListSerializer(serializers.ListSerializer):

    child = StationSerializer()

    def create(self, validated_data):
        books = [Station(**item) for item in validated_data]
        return Station.objects.bulk_create(books)
