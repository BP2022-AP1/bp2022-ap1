import pytest
from traci import vehicle

from src.event_bus.event_bus import EventBus
from src.implementor.models import Run, SimulationConfiguration, Token
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.schedule.schedule import ScheduleConfiguration
from src.spawner.spawner import (
    Spawner,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
)
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Track, Train


@pytest.fixture
def tick():
    return 50


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
def run(simulation_configuration):
    return Run.create(simulation_configuration=simulation_configuration.id)


class MockRouteController:
    method_calls: int = 0

    def recalculate_all_routes(self):
        self.method_calls += 1


@pytest.fixture
def interlocking_disruptor():
    return IInterlockingDisruptor(MockRouteController())


@pytest.fixture
def schedule():
    schedule_configuration = ScheduleConfiguration(
        schedule_type="TrainSchedule",
        strategy_type="RegularScheduleStrategy",
        train_schedule_train_type="cargo",
        regular_strategy_start_tick=10,
        regular_strategy_frequency=100,
    )
    schedule_configuration.save()
    return schedule_configuration


@pytest.fixture
def spawner_configuration(schedule):
    configuration = SpawnerConfiguration()
    configuration.save()
    SpawnerConfigurationXSchedule(
        spawner_configuration_id=configuration.id,
        schedule_configuration_id=schedule.id,
    ).save()
    return configuration


class MockTrainSpawner:
    """Mock class for a TrainSpawner"""


@pytest.fixture
def spawner(spawner_configuration, event_bus):
    spawner = Spawner(
        event_bus=event_bus,
        configuration=spawner_configuration,
        train_spawner=MockTrainSpawner(),
    )
    return spawner
