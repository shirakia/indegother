import datetime
import requests

from rest_framework import status, views
from rest_framework.response import Response

from .models import Station
from .serializers import StationSerializer


class StationCreateAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        now = datetime.datetime.now()

        def call_indego_station_api():
            url = 'https://kiosks.bicycletransit.workers.dev/phl'

            req = requests.get(url)
            return req.json()

        body_json = call_indego_station_api()
        for feature in body_json['features']:
            data = feature['properties']
            data['at'] = now

            serializer = StationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status.HTTP_201_CREATED)
