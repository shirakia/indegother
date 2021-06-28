from rest_framework import serializers, validators

from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        exclude = ['uuid']
        extra_kwargs = {
            'at': {'write_only': True},
        }

    at = serializers.DateTimeField(validators=[validators.UniqueValidator(queryset=Weather.objects.all())])
    document = serializers.DictField()
