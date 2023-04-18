from datetime import datetime
from uuid import uuid4

import pytest

from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
from src.logger.log_collector import LogCollector
from src.logger.logger import Logger


@pytest.fixture
def timestamp():
    return datetime.strptime("2023-04-11-10-00-00", "%Y-%m-%d-%H-%M-%S")


@pytest.fixture
def tick():
    return 50


@pytest.fixture
def message():
    return "Test Log Done"


@pytest.fixture
def token():
    return Token.create(name="user", permission="admin", hashedToken="hash")


@pytest.fixture
def simulation_configuration(token):
    return SimulationConfiguration.create(token=token.id)


@pytest.fixture
def run(simulation_configuration):
    return Run.create(simulation_configuration=simulation_configuration.id)


@pytest.fixture
def logger(run):
    return Logger(run_id=run.id)


@pytest.fixture
def log_collector():
    return LogCollector()


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
def block_section_id():
    return "Test Block Section id"


@pytest.fixture
def block_section_length():
    return 101.53


@pytest.fixture
def platform_blocked_fault_configuration():
    return PlatformBlockedFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="PlatformBlockedFault",
        affected_element_id="12345678",
    )


@pytest.fixture
def track_blocked_fault_configuration():
    return TrackBlockedFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="TrackBlockedFault",
        affected_element_id="12345678",
    )


@pytest.fixture
def track_speed_limit_fault_configuration():
    return TrackSpeedLimitFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="TrackSpeedLimitFault",
        affected_element_id="12345678",
        new_speed_limit=60,
    )


@pytest.fixture
def schedule_blocked_fault_configuration():
    return ScheduleBlockedFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="ScheduleBlockedFault",
        affected_element_id="12345678",
    )


@pytest.fixture
def train_prio_fault_configuration():
    return TrainPrioFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="TrainPrioFault",
        affected_element_id="12345678",
        new_prio=1,
    )


@pytest.fixture
def train_speed_fault_configuration():
    return TrainSpeedFaultConfiguration.create(
        start_tick=1,
        end_tick=100,
        description="TrainSpeedFault",
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
