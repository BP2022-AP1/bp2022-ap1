import os
from collections import defaultdict
from typing import Tuple

import pytest
from traci import constants, edge, simulation, trafficlight, vehicle

from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Signal, Switch, Track, Train
from src.wrapper.train_spawner import TrainSpawner


@pytest.fixture
def results(monkeypatch):
    def get_subscription_result():
        def subscription_results():
            return defaultdict(int)

        dict = defaultdict(subscription_results)
        edge_dict = {
            constants.VAR_POSITION: (
                100,
                100,
            ),
            constants.VAR_ROAD_ID: "cfc57-0",
            constants.VAR_ROUTE: "testing-route",
            constants.VAR_SPEED: 10.2,
        }
        dict["fake-sim-train"] = edge_dict
        return dict

    monkeypatch.setattr(
        simulation, "getAllSubscriptionResults", get_subscription_result
    )


@pytest.fixture
def all_trains(monkeypatch):
    def get_id_list():
        return []

    monkeypatch.setattr(vehicle, "getIDList", get_id_list)


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
    return Edge("cfc57-0")


@pytest.fixture
def edge_re() -> Edge:
    return Edge("cfc57-0-re")


@pytest.fixture
def edge2() -> Edge:
    return Edge("cfc57-1")


@pytest.fixture
def train(train_add, configured_souc: SimulationObjectUpdatingComponent) -> Train:
    # pylint: disable=unused-argument
    created_train = Train(
        identifier="fake-sim-train",
        train_type="fancy-ice",
        timetable=[],
        from_simulator=True,
    )
    created_train.updater = configured_souc
    created_train.update(
        {
            constants.VAR_POSITION: (
                100,
                100,
            ),
            constants.VAR_ROAD_ID: "cfc57-0",
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
def track(edge1: Edge, edge_re: Edge) -> Track:
    return Track(edge1, edge_re)


@pytest.fixture
def switch() -> Switch:
    return Switch(identifier="fancy-switch")


@pytest.fixture
def platform() -> Platform:
    return Platform(
        identifier="fancy-city-platform-1",
        platform_id="fancy-city-platform-1",
        edge_id="cfc57-0",
    )


@pytest.fixture
def souc(traffic_update) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    return SimulationObjectUpdatingComponent()


@pytest.fixture
def configured_souc(
    traffic_update, infrastructure_provider
) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    souc = SimulationObjectUpdatingComponent(
        sumo_configuration=os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        )
    )
    souc.infrastructure_provider = infrastructure_provider
    return souc


@pytest.fixture
def infrastructure_provider() -> SumoInfrastructureProvider:
    class IPMock:
        def train_drove_onto_track(self, train: Train, edge: Edge):
            pass

        def train_drove_off_track(self, edge: Edge):
            pass

    return IPMock()


class MockRouteController:
    def set_spawn_fahrstrasse(self, start: Track, end: Track):
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
