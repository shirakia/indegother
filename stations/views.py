from datetime import datetime
import requests

from rest_framework import status, views
from rest_framework.response import Response

from .models import Station
from .serializers import StationSerializer, StationListSerializer


def call_indego_station_api():
    url = 'https://kiosks.bicycletransit.workers.dev/phl'

    req = requests.get(url)
    return req.json()


class StationCreateAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        now = datetime.now()

        body_json = call_indego_station_api()
        for feature in body_json['features']:
            data = feature['properties']
            data['at'] = now

            serializer = StationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status.HTTP_201_CREATED)


class StationListRetrieveAPIView(views.APIView):

    def get(self, request, *args, **kwargs):
        if 'at' not in request.query_params:
            return Response({'message': "No 'at' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        query_at = request.query_params['at']

        first_station = Station.objects.filter(at__gte=query_at).order_by('at').first()
        if first_station is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        stations = Station.objects.filter(at=first_station.at)

        serializer = StationListSerializer(instance=stations)
        response = {'at': first_station.at, 'stations': serializer.data, 'weather': 'Comming soon'}

        return Response(response, status.HTTP_200_OK)


class StationRetrieveAPIView(views.APIView):

    def get(self, request, kioskId, *args, **kwargs):
        if 'at' not in request.query_params:
            return Response({'message': "No 'at' query parameter"}, status=status.HTTP_400_BAD_REQUEST)
        query_at = request.query_params['at']

        station = Station.objects.filter(at__gte=query_at).order_by('at').filter(kioskId=kioskId).first()
        if station is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StationSerializer(instance=station)
        response = {'at': serializer.data['at'], 'station': serializer.data, 'weather': 'Comming soon'}

        return Response(response, status.HTTP_200_OK)
