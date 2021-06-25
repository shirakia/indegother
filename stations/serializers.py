from rest_framework import serializers
from .models import Station


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ['kioskId', 'at']


class StationListSerializer(serializers.ListSerializer):

    child = StationSerializer()
