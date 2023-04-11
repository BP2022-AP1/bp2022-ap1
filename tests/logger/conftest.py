from datetime import datetime
from uuid import uuid4

import pytest

from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.train_cancelled_fault import (
    TrainCancelledFaultConfiguration,
)
from src.fault_injector.fault_types.train_speed_fault import (
    TrainSpeedFaultConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token


@pytest.fixture
def timestamp():
    return datetime.strptime("2023-04-11-10-00-00", "%Y-%m-%d-%H-%M-%S")


@pytest.fixture
def tick():
    return 50


@pytest.fixture
def message():
    return "Test Log Done"


@pytest.fixture(name="token")
def fixture_token():
    return Token.create(name="user", permission="admin", hashedToken="hash")


@pytest.fixture(name="simulation_configuration")
def fixture_simulation_configuration(token):
    return SimulationConfiguration.create(token=token.id)


@pytest.fixture(name="run")
def fixture_run(simulation_configuration):
    return Run.create(simulation_configuration=simulation_configuration.id)


@pytest.fixture
def train_id():
    return "Test Train id"


@pytest.fixture
def station_id():
    return "Test Station id"


@pytest.fixture
def fahrstrasse():
    return "Test Fahrstrasse"


@pytest.fixture
def signal_id():
    return uuid4()


@pytest.fixture
def state_before():
    return 0


@pytest.fixture
def state_after():
    return 1


@pytest.fixture
def train_speed_fault_configuration():
    return TrainSpeedFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="TrainSpeedFault",
        affected_element_id="12345678",
    )


@pytest.fixture
def platform_blocked_fault_configuration():
    return PlatformBlockedFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="PlatformBlockedFault",
        affected_element_id="12345678",
    )


@pytest.fixture
def train_cancelled_fault_configuration():
    return TrainCancelledFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="TrainCancelledFault",
        affected_element_id="12345678",
    )


@pytest.fixture
def affected_element():
    return "Test Affected Element"


@pytest.fixture
def value_before():
    return "Test Value Before"


@pytest.fixture
def value_after():
    return "Test Value After"
