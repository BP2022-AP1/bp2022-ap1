# bp2022-ap1

|           | `dev`                                                                                                                                                                                                 | `main`                                                                                                                                                                                                  |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CI & CD   | [![CI](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml/badge.svg?branch=dev)](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml?query=branch%3Adev) | [![CI](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/BP2022-AP1/bp2022-ap1/actions/workflows/python-app.yml?query=branch%3Amain) |
| Coveralls | [![Coverage Status](https://coveralls.io/repos/github/BP2022-AP1/bp2022-ap1/badge.svg?branch=dev)](https://coveralls.io/github/BP2022-AP1/bp2022-ap1?branch=dev)                                      | [![Coverage Status](https://coveralls.io/repos/github/BP2022-AP1/bp2022-ap1/badge.svg?branch=main)](https://coveralls.io/github/BP2022-AP1/bp2022-ap1?branch=main)                                      |

A REST API for simulations and analysis of train traffic on the LEAG rail network. Create one of many component configurations, for example, for defining the interlocking, train schedules, and faults. Simulation configurations hold connections to the component configuration. You could add connections to component configurations. A run is the execution of the defined simulation.

**USED TECHNOLOGIES**

- [SUMO](https://sumo.dlr.de/): handles the main simulation logic
- [TraCI](https://sumo.dlr.de/docs/TraCI.html): used to edit a running simulation
- [Celery](https://docs.celeryq.dev/en/stable/): the simulation is executed within a Celery worker
- [peewee](http://docs.peewee-orm.com/en/latest/): interaction with the database
- [Flask](https://flask.palletsprojects.com/en/2.3.x/): used to implement the REST-API
- [yaramo](https://github.com/simulate-digital-rail/yaramo): railway model focusing on interoperability between different existing planning formats

**STRUCTURE OF DOCUMENTATION**

The documentation is structured into three parts: This README, the [Wiki](https://github.com/BP2022-AP1/bp2022-ap1/wiki) and the [documentation of the REST-API](https://bp2022-ap1.github.io/bp2022-ap1/). The following table gives an overview of the content of each part.

| Place                                                              | Content                                                                                                                                                                                                      |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| README                                                             | The readme contains information about the basic development process. That includes the setup, available commands for developers, a description of the environment variables, database management and testing. |
| [Wiki](https://github.com/BP2022-AP1/bp2022-ap1/wiki)              | The wiki introduces the architecture with its components. The other chapters contain descriptions of the components itself.                                                                                 |
| [REST-API documentation](https://bp2022-ap1.github.io/bp2022-ap1/) | The REST-API documentation contains information for the enduser about the interaction with the REST-API. This includes available paths, the allowed request bodies and responses.                                          |

## Setup

We're using `poetry` to manage our dependencies. You can find the documentation of `poetry` here: [poetry documentation](https://python-poetry.org/docs/). To set up this project, you need to install `poetry` and run `poetry install` in the root directory of this project. This will install all dependencies and create a virtual environment. You can activate the virtual environment with a `poetry shell`.

Within the virtual environment, you can run `poe` to run commands. Essential commands are `poe dev` to run the development server and `poe test` to run the tests. You can find more commands in the section Commands. Be sure that you have docker installed.

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

### `poe test-lf`

Run `poe test-lf` to start the test database and run our testing framework for tests that failed last time.

### `poe test-ff`

Run `poe test-ff` to start the test database and run our testing framework, tests that failed last time first.

### `poe test-nf`

Run `poe test-nf` to start the test database and run our testing framework with new tests first.

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

### `poe gui`

Run `poe gui` to start the database and the development server. You can access the endpoint of the REST-API at port 5010. This command disables the celery worker and enables the GUI representation of the simulation.

### `poe insert-config`

Run `poe insert-config` to insert a previously selected config. By default this is one of the configs in `/scripts`.

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

We use `pytest` for testing. You can run the tests with `poe test`. This will also start the test database, drop and recreate all its tables, run the tests and then stop the database container again.

We use `monkeypatch` to mock connections to `TraCI` and `SUMO`.

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
