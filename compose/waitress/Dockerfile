FROM python
WORKDIR /app

RUN pip install poetry


COPY poetry.lock pyproject.toml /app/
RUN poetry install

EXPOSE 8080
COPY . /app
CMD poetry run waitress-serve --call src:create_app
