import os
from collections import defaultdict
from typing import List, Tuple

import pytest
from planpro_importer.reader import PlanProReader
from traci import constants, edge, trafficlight, vehicle

from src.event_bus.event_bus import EventBus
from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.route_controller import (
    TopologyInitializer,
    UninitializedTrain,
)
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Switch, Train
from src.wrapper.train_builder import TrainBuilder


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
    def add_train(identifier, routeID=None, typeID=None):
        # pylint: disable=invalid-name, unused-argument
        # We want to use the same signature as the TraCI methods
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
        ]

    monkeypatch.setattr(vehicle, "subscribe", subscribe_train)


@pytest.fixture
def train_set_route_id(monkeypatch):
    def set_route_id_train(identifier, route_id=None):
        assert identifier is not None
        assert route_id is not None

    monkeypatch.setattr(vehicle, "setRouteID", set_route_id_train)


@pytest.fixture
def train_route_update(monkeypatch):
    def update_route(identifier, routeID=None):
        # pylint: disable=invalid-name
        # We want to use the same signature as the TraCI methods
        assert identifier is not None
        assert routeID is not None

    monkeypatch.setattr(vehicle, "setRouteID", update_route)


@pytest.fixture
def edge1() -> Edge:
    return Edge("bf53d-0")


@pytest.fixture
def edge1_re() -> Edge:
    return Edge("bf53d-0-re")


@pytest.fixture
def edge2() -> Edge:
    return Edge("bf53d-1")


@pytest.fixture
def train(
    train_add,
    train_route_update,
    train_set_route_id,
    max_speed,
    configured_souc: SimulationObjectUpdatingComponent,
    basic_edge1: Edge,
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
            constants.VAR_ROAD_ID: basic_edge1.identifier,
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
    print(created_train.edge.track.identifier)
    print(created_train.edge.track.nodes[0].identifier)
    print(created_train.edge.track.nodes[1].identifier)
    print(isinstance(created_train.edge.track.nodes[1], Switch))
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
    path_name = os.path.join("data", "planpro", "example.ppxml")
    yaramo_topology = PlanProReader(path_name).read_topology_from_plan_pro_file()
    topology_initializer = TopologyInitializer(souc, yaramo_topology)
    topology_initializer.initialize_all()
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

    def set_spawn_fahrstrasse(self, timetable: List[Platform], start: Edge):
        reservation_placeholder = UninitializedTrain(timetable)
        end = timetable[1].edge
        self.set_spawn_fahrstrasse_count += 1
        if start.identifier == "bf53d-0" and end.identifier == "8f9a9-1":
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
    configured_souc: SimulationObjectUpdatingComponent,
    train_add,
    train_subscribe,
    max_speed,
) -> Tuple[SimulationObjectUpdatingComponent, TrainBuilder]:
    # pylint: disable=unused-argument
    return (configured_souc, TrainBuilder(configured_souc, MockRouteController()))


@pytest.fixture
def mocked_event_bus():
    class EventBusMock:
        """Mocks the event bus to test if it gets correctly called"""

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
