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

from lib import utils
from .models import Station
from .serializers import StationListSerializer, StationListWeatherSerializer, StationWeatherSerializer
from weathers.models import Weather
from weathers.serializers import WeatherSerializer


class StationCreateAPIView(views.APIView):

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description=(
            'An endpoints which downloads fresh data from Indego GeoJSON station status API '
            'and stores it inside MongoDB.<br>'
            'This endpoint downloads fresh weather data from Open Weather Map API at the same *at* time<br >'
            '<br>'
            '**Store data only when both Indego and WeatherMapAPI data area valid.**'),
        responses={
            201: OpenApiResponse('201', description='When successfully created'),
            500: OpenApiResponse('500', description='When cannot connect to external API'),
        })
    def post(self, request, *args, **kwargs):
        now = datetime.now()

        try:
            station_json = utils.call_indego_station_api()
        except requests.exceptions.RequestException:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        station_list_data = [{'at': now, 'kioskId': feature['properties']['kioskId'], 'document': feature}
                             for feature in station_json['features']]
        station_list_serializer = StationListSerializer(data=station_list_data)
        station_list_serializer.is_valid(raise_exception=True)

        try:
            weather_json = utils.call_openweathermap_api()
        except requests.exceptions.RequestException:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        weather_data = {'at': now, 'document': weather_json}
        weather_serializer = WeatherSerializer(data=weather_data)
        weather_serializer.is_valid(raise_exception=True)

        # save when both station list and weather are valid
        station_list_serializer.save()
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

    @extend_schema(
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
