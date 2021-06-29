import os
from datetime import datetime
import requests

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse


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

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description=(
            'An endpoints which downloads fresh data from Indego GeoJSON station status API '
            'and stores it inside MongoDB.<br>'
            'This endpoint downloads fresh weather data from Open Weather Map API at the same time of *at*'),
        responses={201: None})
    def post(self, request, *args, **kwargs):
        now = datetime.now()

        station_json = call_indego_station_api()
        for feature in station_json['features']:
            data = {
                'at': now,
                'kioskId': feature['properties']['kioskId'],
                'document': feature,
            }

            station_serializer = StationSerializer(data=data)
            station_serializer.is_valid(raise_exception=True)
            station_serializer.save()

        weather_json = call_openweathermap_api()
        data = {
            'at': now,
            'document': weather_json,
        }
        weather_serializer = WeatherSerializer(data=data)
        weather_serializer.is_valid(raise_exception=True)
        weather_serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class StationListRetrieveAPIView(views.APIView):

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description=(
            'Snapshot of all stations at a specified time.<br>'
            'This endpoint responds with the actual time of the first snapshot of data on '
            'or after the requested time and the data.'),
        request=StationListWeatherSerializer,
        parameters=[
            OpenApiParameter(
                name='at', description='Specific Datetime (e.g. 2019-09-01T10:00:00)', required=True,
                type=str), ],
        responses={
            200: StationListWeatherSerializer,
            400: OpenApiResponse('400', description='When no *at* query parameter'),
            404: OpenApiResponse('404', description='When no stations or no weather for requested *kioskId* and *at*'),  # noqa
        })
    @method_decorator(cache_page(60*60*24))
    @method_decorator(vary_on_headers("Authorization",))
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

    permission_classes = (IsAuthenticated, )

    @ extend_schema(
        description=('Snapshot of one station at a specific time<br>'
                     'The response is the first available on or after the given time.'),
        request=StationWeatherSerializer,
        parameters=[OpenApiParameter(
            name='at', description='Specific Datetime (e.g. 2019-09-01T10:00:00)',
            required=True, type=str), ],
        responses={
            200: StationWeatherSerializer,
            400: OpenApiResponse('400', description='When no *at* query parameter'),
            404: OpenApiResponse('404', description='When no station or no weather for requested *kioskId* and *at*')  # noqa
        })
    @method_decorator(cache_page(60*60*24))
    @method_decorator(vary_on_headers("Authorization",))
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
