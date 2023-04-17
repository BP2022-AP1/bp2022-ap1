import pytest

from src.implementor.models import Run, SimulationConfiguration, Token
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Track


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
def track() -> Track:
    return Track("fault injector track")


@pytest.fixture
def combine_track_and_wrapper(track: Track, wrapper: SimulationObjectUpdatingComponent):
    track.updater = wrapper
    wrapper.simulation_objects.append(track)
    return track, wrapper
