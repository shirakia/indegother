# indegother

Indego station + Open Weather Map

[![CircleCI](https://circleci.com/gh/shirakia/indegother/tree/main.svg?style=svg)](https://circleci.com/gh/shirakia/indegother/tree/main)
[![codecov](https://codecov.io/gh/shirakia/indegother/branch/main/graph/badge.svg?token=MSHF4XNC7K)](https://codecov.io/gh/shirakia/indegother)

## Swagger UI demo

http://54.150.199.176/api/schema/swagger-ui

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
- Django / Django REST framework
- Djongo (Object Document Mapper)
- drf-spectacular (Swagger doc auto generation)

## What I did
- Requirement clarification (Request volume, ambiguas specification, hosting preference)
- Token Authentication
- Implement 3 endpoints as the challenge describes
- Use MongoDB with proper indexes and unique constraints
- Page cache for GET 2 endpoints
- Unit tests for mainly validations
- Functional tests for APIs
- Hosting to an instance of AWS EC2
- API documentation using Swagger
- Use Linter auto correct
- Setup CI(CircleCI for testing, CodeCov for coverage)

## Limitations
- No user registration, no token generation, no token expiration
- No retry for external API request
- Environment variables are hard coded in Dockerfile
- Proper production environment server(https, DNS, load-balancing, separated DB servers, logging, monitoring, proper env variables handling, Same/Cross-origin policy, etc...)
- No deployment automation
