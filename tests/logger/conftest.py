from datetime import datetime

import pytest

from src.implementor.models import Run


@pytest.fixture
def timestamp():
    return datetime.strptime("2023-04-11-10-00-00", "%Y-%m-%d-%H-%M-%S")


@pytest.fixture
def message():
    return "Test Log Done"


@pytest.fixture
def run_as_dict():
    return {}


@pytest.fixture
# pylint: disable=redefined-outer-name # is disabled because used as fixture here
def run(run_as_dict):
    return Run.create(**run_as_dict)


@pytest.fixture
def train_id() -> int:
    return 123


@pytest.fixture
def station_id():
    return 456


@pytest.fixture
def fahrstrasse():
    return "Test Fahrstrasse"


@pytest.fixture
def signal_id():
    return "Test Signal"


@pytest.fixture
def state_before():
    return 0


@pytest.fixture
def state_after():
    return 1


@pytest.fixture
def injection_id():
    return 123


@pytest.fixture
def fault_type():
    return 3


@pytest.fixture
def injection_position():
    return "Test Position"


@pytest.fixture
def duration():
    return 10
