FROM python:3.9.10-slim-buster
LABEL maintainer="my_home.com"

RUN apt-get update

ENV PYTHONUNBUFFERED 1

COPY ./requirements/base.txt /requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 3030

RUN apt-get --yes install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install -r /requirements.txt


