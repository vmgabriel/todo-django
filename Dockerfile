FROM python:3.9.10-slim-buster
LABEL maintainer="my_home.com"

RUN apt-get update

ENV PYTHONUNBUFFERED 1

COPY ./requirements/base.txt /requirements.txt
COPY . /app

WORKDIR /app
EXPOSE 3030

RUN apt-get --yes install libmagic-dev libjpeg-dev\
    zlib1g-dev libjbig0 liblcms2-2 libopenjp2-7\
    libtiff5 libwebp6 libwebpdemux2 libwebpmux3

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install -r /requirements.txt


