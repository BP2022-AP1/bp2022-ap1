import os
from typing import List

import pytest
from traci import trafficlight

from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Signal


@pytest.fixture
def mock_logger():
    class LoggerMock:
        pass

    return LoggerMock()


@pytest.fixture
def configured_souc(traffic_update) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    souc = SimulationObjectUpdatingComponent(
        sumo_configuration=os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        )
    )
    return souc


@pytest.fixture
def traffic_update(monkeypatch):
    rr_count = 0
    gg_count = 0

    def set_traffic_light_state(identifier: str, state: str) -> None:
        # pylint: disable=unused-argument
        nonlocal rr_count, gg_count
        assert state in ("rr", "GG")
        if state == "rr":
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
def route_controller(
    configured_souc: SimulationObjectUpdatingComponent,
) -> RouteController:
    return RouteController(
        simulation_object_updating_component=configured_souc,
        path_name=os.path.join("data", "planpro", "test_example.ppxml"),
    )


@pytest.fixture
def infrastructure_provider(
    route_controller: RouteController,
) -> SumoInfrastructureProvider:
    infrastructure_provider = SumoInfrastructureProvider(route_controller)
    return infrastructure_provider


@pytest.fixture
def yaramo_point():
    class PointMock:
        point_id = "73093"
        state = None

    return PointMock()


@pytest.fixture
def yaramo_signal():
    class SignalMock:
        name = "637cdc98-0b49-4eff-bd2f-b9549becfc57-km-25"
        state = None

    return SignalMock()
