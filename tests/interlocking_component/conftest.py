import os
from typing import List

import pytest

from src.implementor.models import SimulationConfiguration, Token
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
)
from interlocking.interlockinginterface import Interlocking
from traci import trafficlight

from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Signal, Train


@pytest.fixture
def token() -> Token:
    token = Token(name="owner", permission="admin", hashedToken="hash")
    token.save()
    return token


@pytest.fixture
def simulation_configuration() -> SimulationConfiguration:
    config = SimulationConfiguration()
    config.save()
    return config


def interlocking_configuration() -> InterlockingConfiguration:
    config = InterlockingConfiguration(
        dynamicRouting=True,
    )
    config.save()
    return config


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
def sumo_mock_infrastructure_provider(
    route_controller: RouteController,
) -> SumoInfrastructureProvider:
    sumo_mock_infrastructure_provider = SumoInfrastructureProvider(route_controller)
    return sumo_mock_infrastructure_provider


@pytest.fixture
def mock_interlocking() -> Interlocking:
    class InterlockingMock:
        tds_count_in_count = 0
        tds_count_out_count = 0

        def increment_tds_count_in_count(self, track_segment_id):
            self.tds_count_in_count += 1

        def set_tds_count_in_callback(self, infrastructure_provider):
            infrastructure_provider.set_tds_count_in_callback(
                self.increment_tds_count_in_count
            )

        def increment_tds_count_out_count(self, track_segment_id):
            self.tds_count_out_count += 1

        def set_tds_count_out_callback(self, infrastructure_provider):
            infrastructure_provider.set_tds_count_out_callback(
                self.increment_tds_count_out_count
            )

    return InterlockingMock()


@pytest.fixture
def mock_simulation_object_updating_component() -> SimulationObjectUpdatingComponent:
    class SOUCMock:
        infrastructur_provider = None

    return SOUCMock()


@pytest.fixture
def mock_route_controller(
    mock_interlocking: Interlocking,
    mock_simulation_object_updating_component: SimulationObjectUpdatingComponent,
) -> RouteController:
    class RouteControllerMock:
        interlocking: Interlocking = mock_interlocking
        simulation_object_updating_component = mock_simulation_object_updating_component
        maybe_set_fahrstrasse_count = 0
        maybe_free_fahrstrasse_count = 0

        def maybe_set_fahrstrasse(self, train: Train, edge: Edge):
            self.maybe_set_fahrstrasse_count += 1

        def maybe_free_fahrstrasse(self, edge: Edge):
            self.maybe_free_fahrstrasse_count += 1

    return RouteControllerMock()


@pytest.fixture
def interlocking_mock_infrastructure_provider(
    mock_route_controller: RouteController,
) -> SumoInfrastructureProvider:
    interlocking_mock_infrastructure_provider = SumoInfrastructureProvider(
        mock_route_controller
    )
    mock_route_controller.interlocking.set_tds_count_in_callback(
        interlocking_mock_infrastructure_provider
    )
    mock_route_controller.interlocking.set_tds_count_out_callback(
        interlocking_mock_infrastructure_provider
    )
    return interlocking_mock_infrastructure_provider


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


@pytest.fixture
def SUMO_train():
    class TrainMock:
        identifier = "Test_Train"

    return TrainMock()


@pytest.fixture
def SUMO_edge():
    class EdgeMock:
        identifier = "test_id-re"

    return EdgeMock()
