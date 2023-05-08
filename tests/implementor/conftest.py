import pytest

from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.implementor.models import SimulationConfiguration
from src.wrapper.simulation_objects import Edge, Track

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


# ------------- SimulationConfiguration ----------------


@pytest.fixture
def empty_simulation_configuration():
    simulation = SimulationConfiguration()
    simulation.save()
    return simulation
