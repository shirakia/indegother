# Indegother

Indego station + Open Weather Map

[![CircleCI](https://circleci.com/gh/shirakia/indegother/tree/main.svg?style=svg)](https://circleci.com/gh/shirakia/indegother/tree/main)
[![codecov](https://codecov.io/gh/shirakia/indegother/branch/main/graph/badge.svg?token=MSHF4XNC7K)](https://codecov.io/gh/shirakia/indegother)

## Swagger UI demo

1. Go to this url with token
    - http://54.150.199.176/api/schema/swagger-ui

2. Click here!

<kbd>![Screen Shot 0003-06-26 at 22 01 07](https://user-images.githubusercontent.com/728375/123513835-66b7ee00-d6ca-11eb-9af9-7c11cd549864.png)</kbd>

3. Set Token

<kbd>![Screen Shot 0003-06-26 at 22 00 45](https://user-images.githubusercontent.com/728375/123513824-599aff00-d6ca-11eb-98e0-51602cfb2207.png)</kbd>

(For demo server, `Token 8cfb7171617589b8e7bd06c328f921a7697133bd`)

4. Enjoy!

## Run server for development

### Run server

1. Initial set up
```
docker-compose build
docker-compose run web python manage.py createsuperuser
docker-compose run web python manage.py drf_create_token <username>
```

2. Run server
```
docker-compose up
```

3. Go to `http://0.0.0.0:3000/api/schema/swagger-ui/`

## Tech stacks
- Python
- Django / Django REST framework
- Djongo (Object Document Mapper)
- MongoDB
- drf-spectacular (Swagger doc auto generation)

## What I did
- Requirement clarification (Request volume, ambiguas specification, hosting preference)
- For minimum requiements
    - Token Authentication
    - Implement 3 endpoints as the challenge describes
    - Use MongoDB with proper indexes and unique constraints
    - Unit tests for mainly validations and Functional tests for APIs (30 tests for 96% coverage)
    - Hosting to an instance of AWS EC2
    - API documentation using Swagger
- Extras
    - Application-level transaction-like implemenation
    - Return Error codes with custom error classes for front end error handling
    - Page cache for GET 2 endpoints
    - Use Linter auto correct
    - Setup CI(CircleCI for testing, CodeCov for coverage)

## Limitations
- No user registration, no new token generation, no token expiration
- No database-level transactions (I need to pay for Djongo or implement ODM by myself)
- Environment variables are hard coded in Dockerfile
- No proper production server(https, DNS, load-balancing, separated DB servers, logging, monitoring, proper env variables handling, Same/Cross-origin policy, etc...)
- No deployment automation

## Main codes to be reviewed
- Models
    - Station https://github.com/shirakia/indegother/blob/main/stations/models.py
    - Weather https://github.com/shirakia/indegother/blob/main/weathers/models.py
- Serializers
    - Station https://github.com/shirakia/indegother/blob/main/stations/serializers.py
    - Weather https://github.com/shirakia/indegother/blob/main/weathers/serializers.py
    - StationWeather https://github.com/shirakia/indegother/blob/main/stations/station_weather_serializers.py
- Views
    - Station https://github.com/shirakia/indegother/blob/main/stations/views.py
- Tests
    - Station Views      https://github.com/shirakia/indegother/blob/main/stations/tests/test_views.py
    - Station Serializer https://github.com/shirakia/indegother/blob/main/stations/tests/test_serializers.py
    - Weather Serializer https://github.com/shirakia/indegother/blob/main/weathers/tests/test_serializers.py
- Utils
    - Custom Error https://github.com/shirakia/indegother/blob/main/common/errors.py
- Others(less important)
    - utils https://github.com/shirakia/indegother/blob/main/common/utils.py
    - Django setting https://github.com/shirakia/indegother/blob/main/config/settings.py
    - urls https://github.com/shirakia/indegother/blob/main/config/urls.py
    - Dockerfile https://github.com/shirakia/indegother/blob/main/Dockerfile
    - docker-compose.yml https://github.com/shirakia/indegother/blob/main/docker-compose.yml
    - circleci conf https://github.com/shirakia/indegother/blob/main/.circleci/config.yml
