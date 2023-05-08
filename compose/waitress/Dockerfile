FROM python
WORKDIR /app

RUN apt-get update

RUN pip install poetry


COPY . /app
RUN poetry install

EXPOSE 8080
CMD poetry run waitress-serve --call src:create_app
