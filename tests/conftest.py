import os

import pytest

pytest_plugins = [
    "tests.fixtures.fixtures_logger",
    "tests.fixtures.fixtures_model",
    "tests.fixtures.fixtures_spawner",
    "celery.contrib.pytest",
]


@pytest.fixture(scope="session")
def celery_config():
    return {
        "broker_url": os.getenv("CELERY_BROKER_URL", ""),
        "result_backend": os.getenv("CELERY_RESULT_BACKEND", ""),
        "accept_content": [
            "application/json",
            "application/x-python-serialize",
            "pickle",
        ],
        "event_serializer": "pickle",
        "task_serializer": "pickle",
        "result_serializer": "pickle",
    }
