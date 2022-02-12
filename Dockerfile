FROM python:3.9.10-slim-buster
LABEL maintainer="my_home.com"

RUN apt-get update

ENV PYTHONUNBUFFERED 1

COPY ./requirements/base.txt /requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 3030

RUN apt-get --yes install libmagic-dev libjpeg-dev zlib1g-dev libopenjp2-7 libopenjp2-7-dev libopenjp2-tools

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install -r /requirements.txt


