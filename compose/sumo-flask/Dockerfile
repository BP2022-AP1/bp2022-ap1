FROM ubuntu:22.04
WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev software-properties-common

RUN add-apt-repository ppa:sumo/stable
RUN apt-get update && apt-get install -y sumo

RUN pip install poetry

COPY . /app
RUN poetry install
CMD poetry run flask -A src run --debug --host=0.0.0.0