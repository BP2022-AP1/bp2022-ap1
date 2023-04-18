import pytest

from src.implementor.models import Run, SimulationConfiguration, Token
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
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
def run(simulation_configuration):
    return Run.create(simulation_configuration=simulation_configuration.id)


@pytest.fixture
def logger(run):
    return Logger(run_id=run.id)


@pytest.fixture
def interlocking():
    return IInterlockingDisruptor()


@pytest.fixture
def wrapper():
    return SimulationObjectUpdatingComponent()


@pytest.fixture
def edge() -> Edge:
    return Edge("fault injector track")


@pytest.fixture
def edge_re() -> Edge:
    return Edge("fault injector track-re")


@pytest.fixture
def track(edge, edge_re):
    return Track(edge, edge_re)


@pytest.fixture
def combine_track_and_wrapper(track: Track, wrapper: SimulationObjectUpdatingComponent):
    track.updater = wrapper
    wrapper.simulation_objects.append(track)
    return track, wrapper


@pytest.fixture
def combine_platform_and_wrapper(
    platform: Platform, wrapper: SimulationObjectUpdatingComponent
):
    platform.updater = wrapper
    wrapper.simulation_objects.append(platform)
    return platform, wrapper


@pytest.fixture
def combine_train_and_wrapper(train: Train, wrapper: SimulationObjectUpdatingComponent):
    train.updater = wrapper
    wrapper.simulation_objects.append(train)
    return train, wrapper
