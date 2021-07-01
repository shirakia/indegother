from datetime import datetime
import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.dateparse import parse_datetime
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from common import utils
from .models import Station
from .serializers import StationListSerializer
from .station_weather_serializers import StationListWeatherSerializer, StationWeatherSerializer
import errors
from weathers.models import Weather
from weathers.serializers import WeatherSerializer


class StationCreateAPIView(views.APIView):

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description=(
            'An endpoint which downloads fresh data from Indego GeoJSON station status API'
            'and stores it inside MongoDB.<br>'
            'This endpoint downloads fresh weather data from Open Weather Map API at the same time<br><br>'
            '**Stores data only when both Indego and WeatherMapAPI data are valid.**'),
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


def get_at_or_raise(query_params: dict) -> str:
    if 'at' not in query_params:
        raise errors.NoAtError
    try:
        parsed_at = parse_datetime(query_params['at'])
    except ValueError:
        raise errors.InvalidAtError()
    if parsed_at is None:
        raise errors.InvalidAtError()

    return parsed_at


class StationListRetrieveAPIView(views.APIView):

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description=(
            'Snapshot of all stations at a specified time.<br>'
            'This endpoint responds with the actual time of the first snapshot of data on '
            'or after the requested time and the data.<br><br>'
            '**Returns data only when both station list and weather data are found for specified at.**'),
        request=StationListWeatherSerializer,
        parameters=[
            OpenApiParameter(
                name='at', description='Specific Datetime (e.g. 2019-09-01T10:00:00)', required=True,
                type=str), ],
        responses={
            200: StationListWeatherSerializer,
            400: OpenApiResponse('400', description=('When no or invalid *at* query parameter.<br>'
                                                     '**[error_code]** 1000: No *at* query param, 1001: Invalid *at* format')),  # noqa
            404: OpenApiResponse('404', description=('When no stations or no weather for requested *at*.<br>'
                                                     '**[error_code]** 1002: No stations, 1003: No weather'))
        })
    @method_decorator(cache_page(60*60*24))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, *args, **kwargs):
        query_at = get_at_or_raise(request.query_params)

        first_station = Station.objects.filter(at__gte=query_at).order_by('at').first()
        if first_station is None:
            raise errors.StationNotFoundError()

        stations = Station.objects.filter(at=first_station.at)
        weather = Weather.objects.filter(at=first_station.at).first()
        if weather is None:
            raise errors.WeatherNotFoundError()

        serializer = StationListWeatherSerializer({
            'at': first_station.at,
            'stations': stations,
            'weather': weather,
        })

        return Response(serializer.data, status.HTTP_200_OK)


class StationRetrieveAPIView(views.APIView):

    permission_classes = (IsAuthenticated, )

    @extend_schema(
        description=('Snapshot of one station at a specific time.<br>'
                     'The response is the first available on or after the given time.<br><br>'
                     '**Returns data only when both station and weather data are found for specified at.**'),
        request=StationWeatherSerializer,
        parameters=[OpenApiParameter(
            name='at', description='Specific Datetime (e.g. 2019-09-01T10:00:00)',
            required=True, type=str), ],
        responses={
            200: StationWeatherSerializer,
            400: OpenApiResponse('400', description=('When no *at* query parameter.<br>'
                                                     '**[error_code]** 1000: No *at* query param, 1001: Invalid *at* format')),  # noqa
            404: OpenApiResponse('404', description=('When no stations or no weather for requested *kiosId* and *at*.<br>'  # noqa
                                                     '**[error_code]** 1002: No station, 1003: No weather'))
        })
    @method_decorator(cache_page(60*60*24))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, kioskId, *args, **kwargs):
        query_at = get_at_or_raise(request.query_params)

        station = Station.objects.filter(at__gte=query_at).order_by('at').filter(kioskId=kioskId).first()
        if station is None:
            raise errors.StationNotFoundError()
        weather = Weather.objects.filter(at=station.at).first()
        if weather is None:
            raise errors.WeatherNotFoundError()

        serializer = StationWeatherSerializer({
            'at': station.at,
            'station': station,
            'weather': weather,
        })

        return Response(serializer.data, status.HTTP_200_OK)
