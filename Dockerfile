FROM python:3.9.16-slim-bullseye
LABEL maintainer="my_home.com"

ENV PYTHONUNBUFFERED 1

RUN apt-get update --fix-missing && apt-get --yes upgrade

RUN apt-get --yes install libtiff5-dev libjpeg-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev libpq-dev gcc gdal-bin calibre \
    libxml2-dev libxslt1-dev qtbase5-dev python-pyqt5.qtwebengine python3-pyqt5

COPY requirements/base.txt /app/requirements.txt

RUN python3 -m pip install --no-binary lxml lxml
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install -r /app/requirements.txt

COPY . /app

WORKDIR /app
EXPOSE 3030


