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
def simulation_object_updater():
    return SimulationObjectUpdatingComponent()


@pytest.fixture
def edge() -> Edge:
    return Edge("fault injector track")


@pytest.fixture
def edge_re() -> Edge:
    return Edge("fault injector track-re")


@pytest.fixture
def platform() -> Platform:
    return Platform("fancy-platform", platform_id="platform-1", edge_id="fancy-edge")


@pytest.fixture
def track(edge, edge_re):
    track = Track(edge, edge_re)
    edge._track = track
    edge_re._track = track
    return track


@pytest.fixture
def combine_track_and_wrapper(
    track: Track, simulation_object_updater: SimulationObjectUpdatingComponent
):
    track.updater = simulation_object_updater
    simulation_object_updater.simulation_objects.append(track)
    return track, simulation_object_updater


@pytest.fixture
def combine_platform_and_wrapper(
    platform: Platform, simulation_object_updater: SimulationObjectUpdatingComponent
):
    platform.updater = simulation_object_updater
    simulation_object_updater.simulation_objects.append(platform)
    return platform, simulation_object_updater


@pytest.fixture
def combine_train_and_wrapper(
    train: Train, simulation_object_updater: SimulationObjectUpdatingComponent
):
    train.updater = simulation_object_updater
    simulation_object_updater.simulation_objects.append(train)
    return train, simulation_object_updater


@pytest.fixture
def train_add(monkeypatch):
    def add_train(identifier, routeID=None, typeID=None):
        assert identifier is not None
        assert typeID is not None

    monkeypatch.setattr(vehicle, "add", add_train)


@pytest.fixture
# pylint: disable-next=unused-argument
def train(train_add) -> Train:
    return Train(
        identifier="fault injector train",
        train_type="cargo",
        timetable=["platform-1", "platform-2"],
    )


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
