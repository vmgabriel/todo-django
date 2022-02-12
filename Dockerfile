FROM python:3.9-alpine3.13
LABEL maintainer="my_home.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements/base.txt /requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 3030

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg libmagic \
    && pip install Pillow \
    && apk del build-deps

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install -r /requirements.txt


