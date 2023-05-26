from datetime import datetime

import pytest

from src.implementor.models import Run, SimulationConfiguration, Token
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)


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
def simulation_configuration2(token):
    return SimulationConfiguration.create(token=token.id)


@pytest.fixture
def spawner_configuration_x_simulation_configuration(
    spawner_configuration: SpawnerConfiguration,
    simulation_configuration: SimulationConfiguration,
):
    return SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration,
        spawner_configuration=spawner_configuration,
    )


@pytest.fixture
def spawner_configuration_x_demand_schedule(
    spawner_configuration: SpawnerConfiguration,
    demand_train_schedule_configuration: ScheduleConfiguration,
):
    return SpawnerConfigurationXSchedule.create(
        spawner_configuration_id=spawner_configuration.id,
        schedule_configuration_id=demand_train_schedule_configuration.id,
    )


@pytest.fixture
def run(simulation_configuration):
    return Run.create(simulation_configuration=simulation_configuration.id)


@pytest.fixture
def run2(simulation_configuration):
    return Run.create(simulation_configuration=simulation_configuration.id)
