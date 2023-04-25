import os
from typing import Tuple

import pytest
from traci import constants, edge, trafficlight, vehicle

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Switch, Track, Train
from src.wrapper.train_spawner import TrainSpawner


@pytest.fixture
def traffic_update(monkeypatch):
    def set_traffic_light_state(identifier: str, state: str) -> None:
        # pylint: disable=unused-argument
        assert state in ("rr", "GG")

    monkeypatch.setattr(trafficlight, "setRedYellowGreenState", set_traffic_light_state)


@pytest.fixture
def max_speed(monkeypatch):
    def set_max_speed(train_id: str, speed: float):
        assert train_id is not None
        assert speed > 0

    monkeypatch.setattr(vehicle, "setMaxSpeed", set_max_speed)


@pytest.fixture
def speed_update(monkeypatch):
    def set_max_speed(identifier: str, speed: float) -> None:
        assert identifier is not None
        assert speed > 0

    monkeypatch.setattr(edge, "setMaxSpeed", set_max_speed)


@pytest.fixture
def vehicle_route(monkeypatch):
    def set_route_id(train_id: str, route_id: str):
        assert train_id == "fake-sim-train"
        assert route_id == "testing-route-beta"

    monkeypatch.setattr(vehicle, "setRouteID", set_route_id)


@pytest.fixture
def train_add(monkeypatch):
    def add_train(identifier, route, train_type):
        assert identifier is not None
        assert route is not None
        assert train_type is not None

    monkeypatch.setattr(vehicle, "add", add_train)


@pytest.fixture
def edge1() -> Edge:
    return Edge("edge")


@pytest.fixture
def edge_re() -> Edge:
    return Edge("edge-re")


@pytest.fixture
def edge2() -> Edge:
    return Edge("edge2")


@pytest.fixture
def train(train_add) -> Train:
    # pylint: disable=unused-argument
    created_train = Train(
        identifier="fake-sim-train",
        train_type="fancy-ice",
        timetable=[],
        from_simulator=True,
    )
    created_train.update(
        {
            constants.VAR_POSITION: (
                100,
                100,
            ),
            constants.VAR_ROAD_ID: "edge",
            constants.VAR_ROUTE: "testing-route",
            constants.VAR_SPEED: 10.2,
        }
    )
    created_train.train_type.update(
        {
            constants.VAR_MAXSPEED: 11,
        }
    )

    return created_train


@pytest.fixture
def edge(edge1: Edge, edge_re: Edge) -> Track:
    return Track(edge1, edge_re)


@pytest.fixture
def switch() -> Switch:
    return Switch(identifier="fancy-switch")


@pytest.fixture
def platform() -> Platform:
    return Platform(
        identifier="fancy-city-platform-1",
        platform_id="fancy-city-platform-1",
        edge_id="edge",
    )


@pytest.fixture
def souc(traffic_update) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    return SimulationObjectUpdatingComponent()


@pytest.fixture
def configured_souc(traffic_update) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    return SimulationObjectUpdatingComponent(
        sumo_configuration=os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        )
    )


class MockRouteController:
    def set_spawn_route(self, start: Track, end: Track):
        print(start.identifier, end.identifier, start.identifier == "7df3b-1-re")
        if start.identifier == "7df3b-1-re":
            return True
        return False


@pytest.fixture
def spawner(
    configured_souc: SimulationObjectUpdatingComponent, train_add
) -> Tuple[SimulationObjectUpdatingComponent, TrainSpawner]:
    # pylint: disable=unused-argument
    return (configured_souc, TrainSpawner(configured_souc, MockRouteController()))
