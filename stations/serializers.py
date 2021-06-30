from rest_framework import serializers, validators
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from .models import Station
from weathers.serializers import WeatherSerializer


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


class StationListWeatherSerializer(serializers.Serializer):

    class Meta:
        fields = ['at', 'stations', 'weather']

    at = serializers.SerializerMethodField()
    stations = serializers.SerializerMethodField()
    weather = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.DATETIME)
    def get_at(self, obj):
        return obj['at']

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_stations(self, obj):
        serializer = StationListSerializer(instance=obj['stations'])
        return serializer.data

    @extend_schema_field(serializers.DictField())
    def get_weather(self, obj):
        serializer = WeatherSerializer(instance=obj['weather'])
        return serializer.data


class StationWeatherSerializer(serializers.Serializer):

    class Meta:
        fields = ['at', 'station', 'weather']

    at = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()
    weather = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.DATETIME)
    def get_at(self, obj):
        return obj['at']

    @extend_schema_field(serializers.DictField())
    def get_station(self, obj):
        serializer = StationSerializer(instance=obj['station'])
        return serializer.data

    @extend_schema_field(serializers.DictField())
    def get_weather(self, obj):
        serializer = WeatherSerializer(instance=obj['weather'])
        return serializer.data
