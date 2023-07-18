# bp2022-ap1

|           | `dev`                                                                                                                                                                                                 | `main`                                                                                                                                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI & CD   | [![CI](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml/badge.svg?branch=dev)](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml?query=branch%3Adev) | [![CI](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml?query=branch%3Amain) |
| Coveralls | [![Coverage Status](https://coveralls.io/repos/github/BP2022-AP1/bp2022-ap1/badge.svg?branch=dev)](https://coveralls.io/github/BP2022-AP1/bp2022-ap1?branch=dev)                                      | [![Coverage Status](https://coveralls.io/repos/github/BP2022-AP1/bp2022-ap1/badge.svg?branch=main)](https://coveralls.io/github/BP2022-AP1/bp2022-ap1?branch=main)                                      |

TODO: Short introduction to the project

TODO: Short introduction to usage of documentation

## Setup

TODO: Short introduction to setup

## Commands

We're using `poethepoet` to define some handy commands for development. When you're not using the poetry shell, add a `poetry run` before every `poe`.

You can find the documentation of `poe` here: [poe documentation](https://github.com/nat-n/poethepoet)

### `poe format`

Run `poe format` to run `black` and `isort` to format the files.

### `poe lint`

Run `poe lint` to run linting tests on `/src` and `/tests`.

### `poe test`

Run `poe test` to run our testing framework and starting the test database. It uses `poe test-deps` to run the container needed for testing.

### `poe test-deps`

Run `poe test-deps` to run the needed container for tests. These are the test database, a celery-worker, and a redis database.

### `poe ci`

Run `poe ci` to run formatting, linting and testing in preparation for a pull request.

### `poe db`

Run `poe db` to run helper functions for the development and production database. See more about it in Database Management.

### `poe db-test`

Run `poe db-test` to run helper functions for the test database. See more about it in Database Management.

### `poe dev`

Run `poe dev` to start the database, a celery-worker, a redis database, and the development server. You can access the endpoint of the REST-API at port 5010.

### `poe prod`

Run `poe prod` to start the database, celery-worker, a redis database, and the waitress production server. You can access the endpoint of the REST-API at port 8090.

## Environment variables

We're loading public environment variables with docker compose and secret ones with poe. We have four files that contain environment variables.

### `.env.shared`

This file contains harmless public environment variables. They are used by every deployment (test, dev, prod) but can be overriden.

### `.env.test`

This file contains public environment variables for the test environment.

### `.env.dev`

This file contains public environment variables for the dev environment.

### `.env.secret`

This file contains secret variables for the production environment, that shouldn't be shared. It overrides variables from `.env.shared`, `.env.shared` and `os`.

### Important environment variables

- `DISABLE_CELERY` - This variable disables running the simulation in a celery worker and enables the GUI representation of the simulation
- `SUMO_DELAY` - This variable edits the delay time for the GUI representation of the simulation, enabled by `DISABLE_CELERY`.



## PlanPro and SUMO configuration Generator

### PlanPro

There is a ```planpro_helper.py``` in the ```data``` directory, which main method uses yaramo to get a PlanPro file from OSM with hardcoded coordinates. The result is saved into the ```planpro``` subdirectory with a name chosen in ```planpro_helper.py```.

### SUMO configuration

There is a ```sumo_config_helper.py``` in the ```data``` directory, which main method uses yaramo to get a sumo-config from a PlanPro file. The name can not be chosen, but is the one from the input PlanPro file. There is a directory inside the ```sumo``` subdirectory with that name. Inside there is the ```sumo-config```directory with the SUMO files.

By running `bin/db` you can manage the `dev` database and the `test` database.

## Database Management

### Running

Both databases run inside a docker container. Therefore, you have to be part of the `docker` group on linux os. To start one of these containers run `docker compose up postgresql` for the `dev` database or `docker compose up postgresql-test` for the `test` database. The latter should not be necessary because executing `poe test` will automatically run the `test` database, drop and recreate all its tables, run the tests and then stop the database container again.

The dev databases will be available at localhost:5432 and test at localhost:5430.

You can interact with the database content with the `poe db` and `poe db-test` command. The next paragraphs will discuss some commands with `poe db`.

### Creation

If you have started a database for the first time, you need to create its tables. By running `poe db create` the tables of the currently running database will be created.

### Dropping

You can drop all tables of the existing database by executing `poe db drop`.

### Recreating

By running `poe db recreate` all tables of the currently running database will be dropped and then created again.

### Migration

To create a migration for the currently running database execute `poe db migration create <NAME>` where `<NAME>` is an arbitrary name given by you.

You can find the migration file in `db/local/migrations`. You need to implement the changes to the database there (added models, added rows, removed rows, ...). Inside the file are helpful comments.

Afterwards you can run the migration with `poe db migration run <NAME>`.

By running `poe db migration run ALL` you can run all unapplied migrations.

### Rollback

You can rollback the last migration with `poe db rollback`.

## Testing

TODO Short introduction to testing

### Decorators for Database recreation

The decorators `recreate_db` and `recreate_db_setup` are defined in `tests/decorators.py`.

Put `recreate_db` in front of a test function to recreate the db before its execution like this:

```python
from tests.decorators import recreate_db

@recreate_db
def test_function():
    # db will be recreated here
    assert True
```

Put `recreate_db_setup` in front of test setup functions like that:

```python
from tests.decorators import recreate_db_setup

class TestClass:

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_method(self):
        # db will be recreated here
        assert True

    def test_method2(self):
        # db will be recreated here
        assert True
```
