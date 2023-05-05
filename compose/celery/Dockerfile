FROM python
WORKDIR /app

# RUN apt-get update
# RUN apt-get install -y software-properties-common

#RUN add-apt-repository ppa:sumo/stable
RUN apt-get update
RUN apt-get install -y sumo

RUN pip install poetry

COPY . /app
RUN poetry install
CMD poetry run celery -A make_celery worker --loglevel=info
