import os
from datetime import datetime
import requests

from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter


from .models import Station
from .serializers import StationSerializer, StationListWeatherSerializer, StationWeatherSerializer
from weathers.models import Weather
from weathers.serializers import WeatherSerializer


def call_indego_station_api():
    url = 'https://kiosks.bicycletransit.workers.dev/phl'

    req = requests.get(url)
    return req.json()


def call_openweathermap_api():
    appid = os.environ['OPENWEATHERAPI_APPID']
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Philadelphia&appid=' + appid

    req = requests.get(url)
    return req.json()


class StationCreateAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        now = datetime.now()

        station_json = call_indego_station_api()
        for feature in station_json['features']:
            data = feature['properties']
            data['at'] = now

            station_serializer = StationSerializer(data=data)
            station_serializer.is_valid(raise_exception=True)
            station_serializer.save()

        weather_json = call_openweathermap_api()
        weather_json['at'] = now
        weather_serializer = WeatherSerializer(data=weather_json)
        weather_serializer.is_valid(raise_exception=True)
        weather_serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class StationListRetrieveAPIView(views.APIView):

    @extend_schema(request=StationListWeatherSerializer,
                   parameters=[
                       OpenApiParameter(
                           name='at', description='Specific Datetime (e.g. 2019-09-01T10:00:00)',
                           required=True, type=str), ],
                   responses={200: StationListWeatherSerializer, 404: "", })
    def get(self, request, *args, **kwargs):
        if 'at' not in request.query_params:
            return Response({'message': "No 'at' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        query_at = request.query_params['at']

        first_station = Station.objects.filter(at__gte=query_at).order_by('at').first()
        if first_station is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        stations = Station.objects.filter(at=first_station.at)
        weather = get_object_or_404(Weather, at=first_station.at)

        serializer = StationListWeatherSerializer({
            'at': first_station.at,
            'stations': stations,
            'weather': weather,
        })

        return Response(serializer.data, status.HTTP_200_OK)


class StationRetrieveAPIView(views.APIView):

    @extend_schema(request=StationWeatherSerializer,
                   parameters=[
                       OpenApiParameter(
                           name='at', description='Specific Datetime (e.g. 2019-09-01T10:00:00)',
                           required=True, type=str), ],
                   responses={200: StationWeatherSerializer, 404: "", })
    def get(self, request, kioskId, *args, **kwargs):
        if 'at' not in request.query_params:
            return Response({'message': "No 'at' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        query_at = request.query_params['at']

        station = Station.objects.filter(at__gte=query_at).order_by('at').filter(kioskId=kioskId).first()
        if station is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        weather = get_object_or_404(Weather, at=station.at)

        serializer = StationWeatherSerializer({
            'at': station.at,
            'station': station,
            'weather': weather,
        })

        return Response(serializer.data, status.HTTP_200_OK)
