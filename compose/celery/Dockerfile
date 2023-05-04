FROM python
WORKDIR /app

RUN pip install poetry

COPY . /app
RUN poetry install

CMD poetry run celery -A make_celery worker --loglevel=info
