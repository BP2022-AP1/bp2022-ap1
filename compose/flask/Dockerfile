FROM python
WORKDIR /app

RUN pip install poetry

COPY . /app
RUN poetry install

EXPOSE 5000
CMD poetry run flask -A src run --debug --host=0.0.0.0
