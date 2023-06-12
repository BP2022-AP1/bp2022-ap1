import os
from collections import defaultdict
from typing import List, Tuple

import pytest
from traci import constants, edge, trafficlight, vehicle

from src.event_bus.event_bus import EventBus
from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.route_controller import UninitializedTrain
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Switch, Track, Train
from src.wrapper.train_builder import TrainBuilder


@pytest.fixture
def edge2() -> Edge:
    return Edge("a57e4-1")


@pytest.fixture
def train(
    train_add,
    train_route_update,
    configured_souc: SimulationObjectUpdatingComponent,
    edge1: Edge,
) -> Train:
    # pylint: disable=unused-argument
    created_train = Train(
        identifier="fake-sim-train",
        train_type="fancy-ice",
        timetable=[],
        from_simulator=True,
    )
    created_train.train_type.priority = 0
    created_train.updater = configured_souc
    created_train.update(
        {
            constants.VAR_POSITION: (
                100,
                100,
            ),
            constants.VAR_ROAD_ID: "a57e4-0",
            constants.VAR_SPEED: 10.2,
            constants.VAR_STOPSTATE: 0,
        }
    )
    created_train.route = "testing-route"
    created_train.train_type.update(
        {
            constants.VAR_MAXSPEED: 11,
        }
    )
    created_train.reserved_tracks.append(created_train.edge.track)
    created_train.edge.track.reservations.append((created_train, created_train.edge))

    return created_train


@pytest.fixture
def configured_souc(
    traffic_update, infrastructure_provider, mocked_event_bus: EventBus
) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    souc = SimulationObjectUpdatingComponent(
        sumo_configuration=os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        )
    )
    souc.event_bus = mocked_event_bus
    souc.infrastructure_provider = infrastructure_provider
    return souc


@pytest.fixture
def infrastructure_provider() -> SumoInfrastructureProvider:
    class IPMock:
        """Mock for the infrastructure provider"""

        def train_drove_onto_track(self, train: Train, edge: Edge):
            pass

        def train_drove_off_track(self, train: Train, edge: Edge):
            pass

    return IPMock()


class MockRouteController:
    """Mock for the route controller"""

    reserve_for_initialized_train_count = 0
    set_spawn_fahrstrasse_count = 0

    def set_spawn_fahrstrasse(self, timetable: List[Platform]):
        reservation_placeholder = UninitializedTrain(timetable)
        start = timetable[0].edge
        self.set_spawn_fahrstrasse_count += 1
        if start.identifier == "58ab8-1":
            return (True, reservation_placeholder)
        return (False, reservation_placeholder)

    def reserve_for_initialized_train(
        self, reservation_placeholder: UninitializedTrain, train: Train
    ):
        assert isinstance(reservation_placeholder, UninitializedTrain)
        assert isinstance(train, Train)
        self.reserve_for_initialized_train_count += 1


@pytest.fixture
def spawner(
    configured_souc: SimulationObjectUpdatingComponent, train_add, train_subscribe
) -> Tuple[SimulationObjectUpdatingComponent, TrainBuilder]:
    # pylint: disable=unused-argument
    return (configured_souc, TrainBuilder(configured_souc, MockRouteController()))


@pytest.fixture
def mocked_event_bus():
    class EventBusMock:
        spawn_train_calls = 0
        remove_train_calls = 0
        depart_station_calls = 0
        arrive_station_calls = 0

        def spawn_train(self, tick: int, identifier: str):
            assert tick is not None
            assert identifier is not None

            self.spawn_train_calls += 1

        def remove_train(self, tick: int, identifier: str):
            assert tick is not None
            assert identifier is not None

            self.remove_train_calls += 1

        def departure_train(self, tick: int, identifier: str, platform: Platform):
            assert tick is not None
            assert identifier is not None
            assert platform is not None

            self.depart_station_calls += 1

        def arrival_train(self, tick: int, identifier: str, platform: Platform):
            assert tick is not None
            assert identifier is not None
            assert platform is not None

            self.arrive_station_calls += 1

    return EventBusMock()


@pytest.fixture
def mocked_souc(mocked_event_bus: EventBus) -> SimulationObjectUpdatingComponent:
    return SimulationObjectUpdatingComponent(event_bus=mocked_event_bus)
