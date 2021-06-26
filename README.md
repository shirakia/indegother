# indegother

[![CircleCI](https://circleci.com/gh/shirakia/indegother/tree/main.svg?style=svg)](https://circleci.com/gh/shirakia/indegother/tree/main)
[![codecov](https://codecov.io/gh/shirakia/indegother/branch/main/graph/badge.svg?token=MSHF4XNC7K)](https://codecov.io/gh/shirakia/indegother)

## Setup
1. Install Python 3.9.5 and MongoDB
2. `pip install -r requirements.txt`
3. `python generate_secretkey.py > config/local_settings.py` to generate SECRET_KEY for your local env.
4. `python manage.py createsuperuser`
5. `python manage.py drf_create_token <username>` (Set step.4's username here)

## Try API endponts

1. Go to `http://127.0.0.1:8000/api/schema/swagger-ui/`
2. Click here!

![Screen Shot 0003-06-26 at 22 01 07](https://user-images.githubusercontent.com/728375/123513835-66b7ee00-d6ca-11eb-9af9-7c11cd549864.png)


3. Set Token (from Setup.5) 

![Screen Shot 0003-06-26 at 22 00 45](https://user-images.githubusercontent.com/728375/123513824-599aff00-d6ca-11eb-98e0-51602cfb2207.png)

4. Enjoy!
