FROM python:3.7.0 as base

RUN apt-get update && apt-get -y --no-install-recommends install gdal-bin postgresql-client

COPY requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

WORKDIR /ticketbase

FROM base as application
