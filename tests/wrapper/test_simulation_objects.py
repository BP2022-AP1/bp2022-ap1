import pytest
from traci import constants, edge, trafficlight, vehicle

from src.wrapper.simulation_objects import Signal, Track


class TestSignal:
    """Tests for the signal component"""

    @pytest.fixture
    def traffic_update(self, monkeypatch):
        def set_traffic_light_state(identifier: str, state: str) -> None:
            assert identifier == "fancy-signal"
            assert state in ("rr", "GG")

        monkeypatch.setattr(
            trafficlight, "setRedYellowGreenState", set_traffic_light_state
        )

    def test_initial_state(self, traffic_update):
        # pylint: disable=unused-argument
        signal = Signal("fancy-signal")
        assert signal.state == Signal.State.HALT

    def test_update_state(self, traffic_update):
        # pylint: disable=unused-argument
        signal = Signal("fancy-signal")
        signal.state = Signal.State.GO

        assert signal.state == Signal.State.GO


class TestTrack:
    """Tests for the track component"""

    @pytest.fixture
    def track(self):
        return Track("track")

    @pytest.fixture
    def speed_update(self, monkeypatch):
        def set_max_speed(identifier: str, speed: float) -> None:
            assert identifier == "track"
            assert speed == 100

        monkeypatch.setattr(edge, "setMaxSpeed", set_max_speed)

    def test_update_speed(self, track, speed_update):
        # pylint: disable=unused-argument
        track.max_speed = 100

        assert track.max_speed == 100

    def test_default_blocked(self, track):
        assert not track.blocked

    def test_update_blocked(self, track):
        track.blocked = True

        assert track.blocked


class TestTrain:
    """Tests for the train object"""

    @pytest.fixture
    def train(self):
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
                constants.VAR_ROAD_ID: 123,
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
    def vehicle_route(self, monkeypatch):
        def set_route_id(train_id: str, route_id: str):
            assert train_id == "fake-sim-train"
            assert route_id == "testing-route-beta"

        monkeypatch.setattr(vehicle, "setRouteID", set_route_id)

    @pytest.fixture
    def max_speed(self, monkeypatch):
        def set_max_speed(train_id: str, speed: float):
            assert train_id == "fake-sim-train"
            assert speed == 100

        monkeypatch.setattr(vehicle, "setMaxSpeed", set_max_speed)

    @pytest.fixture
    def train_add(self, monkeypatch):
        def add_train(identifier, route, train_type):
            assert identifier == "fancy-rb-001"
            assert route == "not-implemented"
            assert train_type == "fancy-rb"

        monkeypatch.setattr(vehicle, "add", add_train)

    def test_track(self, train):
        assert train.track == 123

    def test_position(self, train):
        assert train.position == (
            100,
            100,
        )

    def test_speed(self, train):
        assert train.speed == 10.2

    def test_route(self, train):
        assert train.route == "testing-route"

    def test_set_route(self, train, vehicle_route):
        # pylint: disable=unused-argument
        train.route = "testing-route-beta"
        assert train.route == "testing-route-beta"

    def test_max_speed(self, train):
        assert train.train_type.max_speed == 11

    def test_set_max_speed(self, train, max_speed):
        # pylint: disable=unused-argument
        train.train_type.max_speed = 100
        assert train.train_type.max_speed == 100

    def test_priority(self, train):
        assert train.train_type.priority == 0

    def test_set_priority(self, train):
        train.train_type.priority = 10
        assert train.train_type.priority == 10

    def test_train_type(self, train):
        assert train.train_type.name == "fancy-ice"

    def test_timetable(self, train):
        assert train.timetable == []

    def test_set_timetable(self, train):
        train.timetable = ["asdf"]
        assert train.timetable == ["asdf"]

    def test_spawning(self, train_add):
        # pylint: disable=unused-argument
        Train(identifier="fancy-rb-001", train_type="fancy-rb")

    def test_update(self, train):
        train.update(
            {
                constants.VAR_POSITION: (
                    110,
                    90,
                ),
                constants.VAR_ROAD_ID: 124,
                constants.VAR_ROUTE: "ending-route",
                constants.VAR_SPEED: 10,
            }
        )
        train.train_type.update(
            {
                constants.VAR_MAXSPEED: 10,
            }
        )
        assert train.track == 124
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

    def test_subscription(self, train):
        assert train.add_subscriptions() > 0
