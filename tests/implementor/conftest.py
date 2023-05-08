import pytest
from traci import vehicle

from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.implementor.models import SimulationConfiguration
from src.wrapper.simulation_objects import Edge, Track, Train

# ------------- TrackSpeedLimitFaultConfiguration ----------------


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
def track_speed_limit_fault_configuration_data(
    track: Track,
) -> dict:
    return {
        "start_tick": 4,
        "end_tick": 130,
        "description": "test TrackSpeedLimitFault",
        "affected_element_id": track.identifier,
        "new_speed_limit": 60,
        "strategy": "regular",
    }


@pytest.fixture
def track_speed_limit_fault_configuration(
    track_speed_limit_fault_configuration_data: dict,
) -> TrackSpeedLimitFaultConfiguration:
    return TrackSpeedLimitFaultConfiguration.create(
        track_speed_limit_fault_configuration_data
    )


# ------------- FaultConfiguration ----------------


@pytest.fixture
def train_add(monkeypatch):
    def add_train(identifier, route, train_type):
        assert identifier is not None
        assert route is not None
        assert train_type is not None

    monkeypatch.setattr(vehicle, "add", add_train)


@pytest.fixture
# pylint: disable-next=unused-argument
def train(train_add) -> Train:
    return Train(identifier="fault injector train", train_type="cargo")


@pytest.fixture
def train_prio_fault_configuration_data(train: Train) -> dict:
    return {
        "start_tick": 50,
        "end_tick": 500,
        "description": "test TrainPrioFault",
        "affected_element_id": train.identifier,
        "new_prio": 3,
        "strategy": "regular",
    }


@pytest.fixture
def train_prio_fault_configuration(train_prio_fault_configuration_data):
    return TrainPrioFaultConfiguration.create(train_prio_fault_configuration_data)


# ------------- SimulationConfiguration ----------------


@pytest.fixture
def empty_simulation_configuration():
    simulation = SimulationConfiguration()
    simulation.save()
    return simulation
