from uuid import uuid4

import pytest
from traci import constants

from src.event_bus.event_bus import EventBus
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import (
    Edge,
    Node,
    Platform,
    Signal,
    Switch,
    Track,
    Train,
)


class TestSignal:
    """Tests for the signal component"""

    def test_initial_state(self, traffic_update):
        # pylint: disable=unused-argument
        signal = Signal("fancy-signal")
        assert signal.state == Signal.State.HALT

    def test_update_state(self, traffic_update):
        # pylint: disable=unused-argument, protected-access
        # We need to set the signal properties manually
        signal = Signal("fancy-signal")
        signal._incoming_index = 0
        signal._controlled_lanes_count = 2
        signal.state = Signal.State.GO

        assert signal.state == Signal.State.GO

    def test_accessible_edges(self):
        signal = Signal("fancy-signal")
        edges = [Edge("a"), Edge("b"), Edge("a-re"), Edge("b-re")]
        signal._edges = edges  # pylint: disable=protected-access

        assert signal.get_edges_accessible_from(edges[0]) == [edges[1], edges[3]]


class TestEdge:
    """Tests for the edge component"""

    def test_update_speed(self, basic_edge1: Edge):
        basic_edge1.max_speed = 100

        assert basic_edge1.max_speed == 100

    def test_default_blocked(self, basic_edge1: Edge):
        assert not basic_edge1.blocked

    def test_update_blocked(self, basic_edge1: Edge):
        basic_edge1.blocked = True

        assert basic_edge1.blocked


class TestNode:
    """Tests for the node abstract class"""

    def test_accessible_edges(self):
        node = Node("fancy-node")
        node._edges = ["a", "b"]  # type: ignore # pylint: disable=protected-access

        assert node.get_edges_accessible_from("a") == ["a", "b"]


class TestTrack:
    """Tests the track component"""

    def test_update_speed(self, basic_track: Track):
        basic_track.max_speed = (100, 200)
        assert basic_track.edges[0].max_speed == 100
        assert basic_track.edges[1].max_speed == 200
        assert basic_track.max_speed == (100, 200)

        basic_track.max_speed = 150
        assert basic_track.edges[0].max_speed == 150
        assert basic_track.edges[1].max_speed == 150
        assert basic_track.max_speed == 150

    def test_blocked(self, basic_track: Track):
        basic_track.blocked = (True, False)
        assert basic_track.edges[0].blocked
        assert not basic_track.edges[1].blocked
        assert basic_track.blocked == (True, False)

        basic_track.blocked = True
        assert basic_track.edges[0].blocked
        assert basic_track.edges[1].blocked
        assert basic_track.blocked

    def test_length(self, basic_track: Track):
        # pylint: disable=protected-access
        basic_track.edges[0]._length = 100
        basic_track.edges[1]._length = 100
        assert (
            basic_track.length
            == basic_track.edges[0].length
            == basic_track.edges[1].length
        )


class TestTrain:
    """Tests for the train object"""

    def test_edge(
        self, train: Train, souc: SimulationObjectUpdatingComponent, basic_edge1: Edge
    ):
        souc.simulation_objects.append(train)

        train.updater = souc
        basic_edge1.updater = souc

        assert train.edge.identifier == basic_edge1.identifier

    def test_position(self, train: Train):
        assert train.position == (
            100,
            100,
        )

    def test_speed(self, train: Train):
        assert train.speed == 10.2

    def test_route(self, train: Train):
        assert train.route == "testing-route"

    def test_set_route(self, train: Train, vehicle_route):
        # pylint: disable=unused-argument
        train.route = "testing-route-beta"
        assert train.route == "testing-route-beta"

    def test_max_speed(self, train: Train):
        assert train.train_type.max_speed == 11

    def test_set_max_speed(self, train: Train, max_speed):
        # pylint: disable=unused-argument
        train.train_type.max_speed = 100
        assert train.train_type.max_speed == 100

    def test_priority(self, train: Train):
        assert train.train_type.priority == 0

    def test_set_priority(self, train: Train):
        train.train_type.priority = 10
        assert train.train_type.priority == 10

    def test_train_type(self, train: Train):
        assert train.train_type.name == "fancy-ice"

    def test_timetable(self, train: Train):
        assert train.timetable == []

    def test_set_timetable(self, train: Train):
        train.timetable = ["asdf"]
        assert train.timetable == ["asdf"]

    def test_spawning(self, mocked_event_bus, mocked_souc, train_add):
        # pylint: disable=unused-argument
        Train(
            identifier="fancy-rb-001",
            train_type="fancy-rb",
            updater=mocked_souc,
            timetable=["platform-1", "platform-2"],
        )

        assert mocked_event_bus.spawn_train_calls == 1

    def test_update(
        self,
        configured_souc: SimulationObjectUpdatingComponent,
        train: Train,
        edge2: Edge,
    ):
        train.updater = configured_souc
        edge2.updater = configured_souc

        configured_souc.simulation_objects.append(train)
        configured_souc.simulation_objects.append(edge2)

        train.update(
            {
                constants.VAR_POSITION: (
                    110,
                    90,
                ),
                constants.VAR_ROAD_ID: "a57e4-1",
                constants.VAR_SPEED: 10,
                constants.VAR_STOPSTATE: 0,
            }
        )
        train.route = "ending-route"
        train.train_type.update(
            {
                constants.VAR_MAXSPEED: 10,
            }
        )

        assert train.edge.identifier == edge2.identifier
        assert train.position == (
            110,
            90,
        )
        assert train.speed == 10
        assert train.train_type.max_speed == 10
        assert train.route == "ending-route"
        assert train.train_type.priority == 0
        assert train.train_type.name == "fancy-ice"
        assert train.timetable == []

    def test_subscription(self, train: Train):
        assert len(train.add_subscriptions()) > 0

    def test_spawn_loaded_net(
        self, configured_souc: SimulationObjectUpdatingComponent, train_add
    ):
        # pylint: disable=unused-argument
        p1_id = Platform("station-1", edge_id="a57e4-1", platform_id="station-1")
        p2_id = Platform("station-2", edge_id="58ab8-2", platform_id="station-2")

        Train(
            identifier=f"{uuid4()}_42",
            timetable=[p1_id, p2_id],
            train_type="cargo",
            updater=configured_souc,
        )

    def test_current_platform(
        self,
        configured_souc: SimulationObjectUpdatingComponent,
        train_add,
        mocked_event_bus: EventBus,
    ):
        # pylint: disable=unused-argument
        p1_id = Platform("station-1", edge_id="a57e4-0", platform_id="station-1")
        p1_id.updater = configured_souc
        p2_id = Platform("station-2", edge_id="a57e4-1", platform_id="station-2")
        p2_id.updater = configured_souc

        train = Train(
            identifier=f"{uuid4()}_42",
            timetable=[p1_id, p2_id],
            train_type="cargo",
            updater=configured_souc,
        )

        assert train.current_platform is not None and train.current_platform == p1_id

        train.update(
            {
                constants.VAR_POSITION: (0, 0),
                constants.VAR_ROAD_ID: "a57e4-0",
                constants.VAR_SPEED: 10,
                constants.VAR_STOPSTATE: 16,  # set the isBusStop bit to 1
            }
        )

        train.update(
            {
                constants.VAR_POSITION: (0, 0),
                constants.VAR_ROAD_ID: "a57e4-0",
                constants.VAR_SPEED: 10,
                constants.VAR_STOPSTATE: 0,  # set the isBusStop bit to 0
            }
        )

        assert train.current_platform is not None and train.current_platform == p2_id

        train.update(
            {
                constants.VAR_POSITION: (0, 0),
                constants.VAR_ROAD_ID: "a57e4-0",
                constants.VAR_SPEED: 10,
                constants.VAR_STOPSTATE: 16,  # set the isBusStop bit to 1
            }
        )

        assert mocked_event_bus.depart_station_calls == 1
        assert mocked_event_bus.arrive_station_calls == 2


class TestSwitch:
    """Tests for the switch object"""

    def test_state(self, basic_switch: Switch):
        assert basic_switch.state == Switch.State.LEFT
        basic_switch.state = Switch.State.RIGHT
        assert basic_switch.state == Switch.State.RIGHT

    def test_invalid_state(self, basic_switch: Switch):
        def bad_state():
            basic_switch.state = "left"

        pytest.raises(ValueError, bad_state)

    def test_update(self, basic_switch: Switch):
        basic_switch.update({"state": "right"})
        assert basic_switch.state == Switch.State.LEFT

    def test_subscription(self, basic_switch: Switch):
        assert len(basic_switch.add_subscriptions()) == 0


class TestPlatform:
    """Tests for the platform object"""

    def test_edge(
        self,
        basic_platform: Platform,
        basic_edge1: Edge,
    ):
        assert basic_platform.edge.identifier == basic_edge1.identifier

    def test_platform_id(self, basic_platform: Platform):
        assert basic_platform.platform_id == "platform-1"

    def test_update(self, basic_platform: Platform):
        basic_platform.update({})
        assert basic_platform.platform_id == "platform-1"

    def test_subscription(self, basic_platform: Platform):
        assert len(basic_platform.add_subscriptions()) == 0
