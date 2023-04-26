FROM python
WORKDIR /app

RUN pip install poetry


COPY poetry.lock pyproject.toml /app/
RUN poetry install

COPY . /app
EXPOSE 5000
CMD poetry run flask -A src run --debug --host=0.0.0.0
