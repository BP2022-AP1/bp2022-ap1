import os
from typing import Type

import pytest
from interlocking.interlockinginterface import Interlocking
from traci import trafficlight, vehicle

from src.event_bus.event_bus import EventBus
from src.implementor.models import SimulationConfiguration, Token
from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
)
from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Signal, Train


@pytest.fixture
def mock_event_bus() -> EventBus:
    class EventBusMock:
        """This mocks the EventBus and counts how often the logging methods are called."""

        create_fahrstrasse_count = 0
        remove_fahrstrasse_count = 0
        set_signal_go_count = 0
        set_signal_halt_count = 0
        train_enter_block_section_count = 0
        train_leave_block_section_count = 0

        # The following methods must implement the interface of those methods in the real classes
        # pylint: disable=unused-argument
        def create_fahrstrasse(self, tick: int, fahrstrasse: str) -> Type[None]:
            self.create_fahrstrasse_count += 1

        def remove_fahrstrasse(self, tick: int, fahrstrasse: str) -> Type[None]:
            self.remove_fahrstrasse_count += 1

        def set_signal(
            self, tick: int, signal_id: str, state_before: int, state_after: int
        ) -> Type[None]:
            if state_after == Signal.State.GO:
                self.set_signal_go_count += 1
            elif state_after == Signal.State.HALT:
                self.set_signal_halt_count += 1

        def train_enter_block_section(
            self,
            tick: int,
            train_id: str,
            block_section_id: str,
            block_section_length: float,
        ) -> Type[None]:
            self.train_enter_block_section_count += 1

        def train_leave_block_section(
            self,
            tick: int,
            train_id: str,
            block_section_id: str,
            block_section_length: float = 0,
        ) -> Type[None]:
            self.train_leave_block_section_count += 1

        # pylint: enable=unused-argument

    return EventBusMock()


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


@pytest.fixture
def unsaved_simulation_configuration() -> SimulationConfiguration:
    return SimulationConfiguration.create()


@pytest.fixture
def interlocking_configuration() -> InterlockingConfiguration:
    config = InterlockingConfiguration(
        dynamicRouting=True,
    )
    config.save()
    return config


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
    configured_souc: SimulationObjectUpdatingComponent, mock_event_bus: EventBus
) -> RouteController:
    return RouteController(
        event_bus=mock_event_bus,
        priority=1,
        simulation_object_updating_component=configured_souc,
        path_name=os.path.join("data", "planpro", "test_example.ppxml"),
    )


@pytest.fixture
def sumo_mock_infrastructure_provider(
    route_controller: RouteController, mock_event_bus: EventBus
) -> SumoInfrastructureProvider:
    sumo_mock_infrastructure_provider = SumoInfrastructureProvider(
        route_controller, mock_event_bus
    )
    return sumo_mock_infrastructure_provider


@pytest.fixture
def mock_interlocking() -> Interlocking:
    class InterlockingMock:
        """This mocks the interlocking and counts how often
        tds_count_in_count and tds_count_out_count are called.
        """

        tds_count_in_count = 0
        tds_count_out_count = 0

        # In the infrastructureProvieder the callbacks are called
        # with track_segment_id as an argument. This is why they need to be here.
        # pylint: disable=unused-argument
        def increment_tds_count_in_count(self, track_segment_id):
            self.tds_count_in_count += 1

        def increment_tds_count_out_count(self, track_segment_id):
            self.tds_count_out_count += 1

        # pylint: enable=unused-argument

        # protected-access has to be disabled, because setting the
        # callbacks does not really work like a private method.
        # pylint: disable=protected-access
        def set_tds_count_in_callback(self, infrastructure_provider):
            infrastructure_provider._set_tds_count_in_callback(
                self.increment_tds_count_in_count
            )

        def set_tds_count_out_callback(self, infrastructure_provider):
            infrastructure_provider._set_tds_count_out_callback(
                self.increment_tds_count_out_count
            )

        # pylint: enable=protected-access

    return InterlockingMock()


@pytest.fixture
def mock_simulation_object_updating_component() -> SimulationObjectUpdatingComponent:
    class SOUCMock:
        """This mocks a simulation object updating component
        with an infrastructur_provider that may be set.
        """

        infrastructur_provider = None

    return SOUCMock()


@pytest.fixture
def mock_route_controller(
    mock_interlocking: Interlocking,
    configured_souc: SimulationObjectUpdatingComponent,
) -> RouteController:
    class RouteControllerMock:
        """This mocks the route controller in a way,
        that counts how often each method was called.
        """

        interlocking: Interlocking = mock_interlocking
        simulation_object_updating_component = configured_souc
        maybe_set_fahrstrasse_count = 0
        maybe_free_fahrstrasse_count = 0

        # The following methods must implement the interface of those methods in the real classes
        # pylint: disable=unused-argument
        def maybe_set_fahrstrasse(self, train: Train, edge: Edge):
            self.maybe_set_fahrstrasse_count += 1

        def maybe_free_fahrstrasse(self, train: Train, edge: Edge):
            self.maybe_free_fahrstrasse_count += 1

        # pylint: enable=unused-argument

    return RouteControllerMock()


@pytest.fixture
def interlocking_mock_infrastructure_provider(
    mock_route_controller: RouteController, event_bus: EventBus
) -> SumoInfrastructureProvider:
    interlocking_mock_infrastructure_provider = SumoInfrastructureProvider(
        mock_route_controller, event_bus
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
        """This mocks a point (or switch) coming from yaramo/the interlocking
        with the same attributes, but not the functionality.
        """

        point_id = "73093"
        state = None

    return PointMock()


@pytest.fixture
def yaramo_signal():
    class SignalMock:
        """This mocks a signal coming from yaramo/the interlocking
        with the same attributes, but not the functionality.
        """

        name = "637cdc98-0b49-4eff-bd2f-b9549becfc57-km-25"
        state = None

    return SignalMock()


@pytest.fixture
def sumo_train() -> Train:
    class TrainMock:
        """This mocks a train coming from SUMO with the same attributes,
        but not the functionality.
        """

        identifier = "Test_Train"

    return TrainMock()


@pytest.fixture
def sumo_edge() -> Edge:
    class EdgeMock:
        """This mocks an edge coming from SUMO with the same attributes,
        but not the functionality.
        """

        identifier = "test_id-re"

    return EdgeMock()


@pytest.fixture
def train_add(monkeypatch):
    def add_train(identifier, route, train_type):
        assert identifier is not None
        assert route is not None
        assert train_type is not None

    monkeypatch.setattr(vehicle, "add", add_train)
