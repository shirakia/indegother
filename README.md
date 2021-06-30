# indegother

Indego station + Open Weather Map

[![CircleCI](https://circleci.com/gh/shirakia/indegother/tree/main.svg?style=svg)](https://circleci.com/gh/shirakia/indegother/tree/main)
[![codecov](https://codecov.io/gh/shirakia/indegother/branch/main/graph/badge.svg?token=MSHF4XNC7K)](https://codecov.io/gh/shirakia/indegother)

## Swagger UI demo

http://54.150.199.176/api/schema/swagger-ui

Go with this token `Token 8cfb7171617589b8e7bd06c328f921a7697133bd`

## Setup and Run server
1. Install docker
2. `docker-compose build`
3. `docker-compose run web python manage.py createsuperuser`
4. `docker-compose run web python manage.py drf_create_token <username>`
5. `docker-compose up`

## Try API endponts

1. Go to `http://127.0.0.1:8000/api/schema/swagger-ui/`
2. Click here!

<kbd>![Screen Shot 0003-06-26 at 22 01 07](https://user-images.githubusercontent.com/728375/123513835-66b7ee00-d6ca-11eb-9af9-7c11cd549864.png)</kbd>

3. Set Token (from Setup.5) 

<kbd>![Screen Shot 0003-06-26 at 22 00 45](https://user-images.githubusercontent.com/728375/123513824-599aff00-d6ca-11eb-98e0-51602cfb2207.png)</kbd>

4. Enjoy!

## Tech stacks
- Python
- Django / Django REST framework
- Djongo (Object Document Mapper)
- MongoDB
- drf-spectacular (Swagger doc auto generation)

## What I did
- Minimum requirement clarification (Request volume, ambiguas specification, hosting preference)
- Token Authentication
- Implement 3 endpoints as the challenge describes
- Use MongoDB with proper indexes and unique constraints
- Application-level transaction-like implemenation
- Page cache for GET 2 endpoints
- Unit tests for mainly validations and Functional tests for APIs (27 tests for 95% coverage)
- Hosting to an instance of AWS EC2
- API documentation using Swagger
- Use Linter auto correct
- Setup CI(CircleCI for testing, CodeCov for coverage)

## Limitations
- No user registration, no token generation, no token expiration
- No retry for external API request
- No database-level transactions
- Environment variables are hard coded in Dockerfile
- Proper production environment server(https, DNS, load-balancing, separated DB servers, logging, monitoring, proper env variables handling, Same/Cross-origin policy, etc...)
- No deployment automation

## Main codes to be reviewed
- Models
    - Station https://github.com/shirakia/indegother/blob/main/stations/models.py
    - Weather https://github.com/shirakia/indegother/blob/main/weathers/models.py
- Serializers
    - Station https://github.com/shirakia/indegother/blob/main/stations/serializers.py
    - Weather https://github.com/shirakia/indegother/blob/main/weathers/serializers.py
- Views
    - Station https://github.com/shirakia/indegother/blob/main/stations/views.py
- Tests
    - Station Views      https://github.com/shirakia/indegother/blob/main/stations/tests/test_views.py
    - Station Serializer https://github.com/shirakia/indegother/blob/main/stations/tests/test_serializers.py
    - Weather Serializer https://github.com/shirakia/indegother/blob/main/weathers/tests/test_serializers.py
- Others(less important)
    - utils https://github.com/shirakia/indegother/blob/main/common/utils.py
    - Django setting https://github.com/shirakia/indegother/blob/main/config/settings.py
    - urls https://github.com/shirakia/indegother/blob/main/config/urls.py
    - Dockerfile https://github.com/shirakia/indegother/blob/main/Dockerfile
    - docker-compose.yml https://github.com/shirakia/indegother/blob/main/docker-compose.yml
    - circleci conf https://github.com/shirakia/indegother/blob/main/.circleci/config.yml
