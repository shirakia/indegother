FROM python:3.9.5

ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY !w714c59b(v_m8v6fq8#)%g-ub^qs-in-0a9i5ls7yxcxvz$=j
ENV OPENWEATHERAPI_APPID e74a3d24fcb83ed98d1a53d5f72ad51c
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
