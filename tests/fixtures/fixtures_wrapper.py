import os
from collections import defaultdict
from typing import Tuple

import pytest
from traci import constants, edge, trafficlight, vehicle

from src.event_bus.event_bus import EventBus
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Switch, Track, Train

############################################# traci monkeypatching


@pytest.fixture
def results(monkeypatch):
    def get_subscription_result():
        def subscription_results():
            return defaultdict(int)

        dict_ = defaultdict(subscription_results)
        edge_dict = defaultdict(int)
        edge_dict[constants.VAR_ROAD_ID] = "bf53d-0"  # type: ignore
        dict_["fake-sim-train"] = edge_dict
        return dict_

    monkeypatch.setattr(vehicle, "getAllSubscriptionResults", get_subscription_result)


@pytest.fixture
def all_trains(monkeypatch):
    def get_id_list():
        return []

    monkeypatch.setattr(vehicle, "getIDList", get_id_list)


@pytest.fixture
def traffic_update(monkeypatch):
    rr_count = 0
    gg_count = 0

    def set_traffic_light_state(identifier: str, state: str) -> None:
        # pylint: disable=unused-argument
        nonlocal rr_count, gg_count
        assert state in ("rG", "GG")
        if state == "rG":
            rr_count += 1
        else:
            gg_count += 1

    def get_rr_count() -> int:
        return rr_count

    def get_gg_count() -> int:
        return gg_count

    monkeypatch.setattr(trafficlight, "setRedYellowGreenState", set_traffic_light_state)

    return (get_rr_count, get_gg_count)


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
def train_add(monkeypatch, max_speed):
    # pylint: disable=unused-argument
    def add_train(identifier, routeID=None, typeID=None):
        assert identifier is not None
        assert typeID is not None

    monkeypatch.setattr(vehicle, "add", add_train)


@pytest.fixture
def train_subscribe(monkeypatch):
    def subscribe_train(identifier, subscriptions=None):
        assert identifier is not None
        assert subscriptions == [
            constants.VAR_POSITION,
            constants.VAR_ROAD_ID,
            constants.VAR_SPEED,
            constants.VAR_STOPSTATE,
        ]

    monkeypatch.setattr(vehicle, "subscribe", subscribe_train)


@pytest.fixture
def train_route_update(monkeypatch):
    def update_route(identifier, routeID=None):
        assert identifier is not None
        assert routeID is not None

    monkeypatch.setattr(vehicle, "setRouteID", update_route)


##################################### mocks


@pytest.fixture
def souc(traffic_update, event_bus: EventBus) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    return SimulationObjectUpdatingComponent(
        event_bus=event_bus,
    )


@pytest.fixture
def event_bus(run) -> EventBus:
    bus = EventBus(run_id=run.id)
    Logger(event_bus=bus)
    return bus


@pytest.fixture
def basic_train(souc: SimulationObjectUpdatingComponent, train_add, max_speed) -> Train:
    # pylint: disable=unused-argument
    train = Train(
        identifier="basic-train",
        train_type="cargo",
        updater=souc,
        timetable=[],
    )
    souc.simulation_objects.append(train)
    return train


@pytest.fixture
def basic_edge1(souc: SimulationObjectUpdatingComponent, speed_update) -> Edge:
    # pylint: disable=unused-argument
    edge = Edge("bf53d-0")
    edge.updater = souc
    souc.simulation_objects.append(edge)
    return edge


@pytest.fixture
def basic_edge1_re(souc: SimulationObjectUpdatingComponent, speed_update) -> Edge:
    # pylint: disable=unused-argument
    edge = Edge("bf53d-0-re")
    edge.updater = souc
    souc.simulation_objects.append(edge)
    return edge


@pytest.fixture
def basic_track(
    basic_edge1: Edge, basic_edge1_re: Edge, souc: SimulationObjectUpdatingComponent
) -> Track:
    track = Track(basic_edge1, basic_edge1_re)
    track.updater = souc
    souc.simulation_objects.append(track)
    return track


@pytest.fixture
def basic_platform(
    basic_edge1: Edge, souc: SimulationObjectUpdatingComponent
) -> Platform:
    platform = Platform(
        identifier="basic-platform",
        platform_id="platform-1",
        edge_id=basic_edge1.identifier,
    )
    platform.updater = souc
    souc.simulation_objects.append(platform)
    return platform


@pytest.fixture
def basic_switch(souc: SimulationObjectUpdatingComponent) -> Switch:
    switch = Switch(identifier="basic-switch")
    switch.updater = souc
    souc.simulation_objects.append(switch)
    return switch
