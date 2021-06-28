from rest_framework import serializers
from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        exclude = ['uuid']
        extra_kwargs = {
            'at': {'write_only': True},
        }

    document = serializers.DictField()
