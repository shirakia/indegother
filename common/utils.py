import os
import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter


def call_external_api(url: str) -> str:
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    header = {'content-type': "Application/json"}
    response = session.get(url=url, headers=header, stream=True, timeout=(10.0, 30.0))
    response.raise_for_status()
    return response.json()


def call_indego_station_api() -> str:
    url = 'https://kiosks.bicycletransit.workers.dev/phl'
    return call_external_api(url)


def call_openweathermap_api() -> str:
    appid = os.environ['OPENWEATHERAPI_APPID']
    url = 'https://api.openweathermap.org/data/2.5/weather?q=Philadelphia&appid=' + appid
    return call_external_api(url)
