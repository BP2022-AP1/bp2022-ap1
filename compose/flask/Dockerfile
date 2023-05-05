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

EXPOSE 5000
CMD poetry run flask -A src run --debug --host=0.0.0.0
