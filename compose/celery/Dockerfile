FROM python
WORKDIR /app

RUN pip install poetry


COPY poetry.lock pyproject.toml /app/
RUN poetry install

COPY . /app
CMD poetry run celery -A make_celery worker --loglevel=info
