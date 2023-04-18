from uuid import uuid4

import pytest
from traci import constants, edge, trafficlight, vehicle

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Platform, Signal, Switch, Track, Train


@pytest.fixture
def traffic_update(monkeypatch):
    def set_traffic_light_state(identifier: str, state: str) -> None:
        # pylint: disable=unused-argument
        assert state in ("rr", "GG")

    monkeypatch.setattr(trafficlight, "setRedYellowGreenState", set_traffic_light_state)


@pytest.fixture
def track():
    return Track("track")


@pytest.fixture
def track2():
    return Track("track2")


@pytest.fixture
def speed_update(monkeypatch):
    def set_max_speed(identifier: str, speed: float) -> None:
        assert identifier == "track"
        assert speed == 100

    monkeypatch.setattr(edge, "setMaxSpeed", set_max_speed)


@pytest.fixture
def train(train_add):
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
            constants.VAR_ROAD_ID: "track",
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
def vehicle_route(monkeypatch):
    def set_route_id(train_id: str, route_id: str):
        assert train_id == "fake-sim-train"
        assert route_id == "testing-route-beta"

    monkeypatch.setattr(vehicle, "setRouteID", set_route_id)


@pytest.fixture
def max_speed(monkeypatch):
    def set_max_speed(train_id: str, speed: float):
        assert train_id == "fake-sim-train"
        assert speed == 100

    monkeypatch.setattr(vehicle, "setMaxSpeed", set_max_speed)


@pytest.fixture
def train_add(monkeypatch):
    def add_train(identifier, route, train_type):
        assert identifier is not None
        assert route is not None
        assert train_type is not None

    monkeypatch.setattr(vehicle, "add", add_train)


@pytest.fixture
def switch():
    return Switch(identifier="fancy-switch")


@pytest.fixture
def platform() -> Platform:
    return Platform(
        identifier="fancy-city-platform-1",
        platform_id="fancy-city-platform-1",
        track_id="track",
    )


@pytest.fixture
def souc(traffic_update) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    return SimulationObjectUpdatingComponent()


@pytest.fixture
def configured_souc(traffic_update) -> SimulationObjectUpdatingComponent:
    # pylint: disable=unused-argument
    return SimulationObjectUpdatingComponent(
        sumo_configuration="sumo-config/example.scenario.sumocfg"
    )


class TestSignal:
    """Tests for the signal component"""

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

    def test_track(self, train, souc, track):
        souc.simulation_objects.append(train)
        souc.simulation_objects.append(track)

        train.updater = souc
        track.updater = souc

        assert train.track == track

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

    def test_update(self, souc, train, track2):
        train.updater = souc
        track2.updater = souc

        souc.simulation_objects.append(train)
        souc.simulation_objects.append(track2)

        train.update(
            {
                constants.VAR_POSITION: (
                    110,
                    90,
                ),
                constants.VAR_ROAD_ID: "track2",
                constants.VAR_ROUTE: "ending-route",
                constants.VAR_SPEED: 10,
            }
        )
        train.train_type.update(
            {
                constants.VAR_MAXSPEED: 10,
            }
        )

        assert train.track == track2
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

    def test_spawn_loaded_net(self, configured_souc, train_add):
        # pylint: disable=unused-argument
        p1_id = "station-1"
        p2_id = "station-2"

        Train(
            identifier=f"{uuid4()}_42",
            timetable=[p1_id, p2_id],
            train_type="cargo",
            updater=configured_souc,
        )


class TestSwitch:
    """Tests for the switch object"""

    def test_state(self, switch):
        assert switch.state == Switch.State.LEFT
        switch.state = Switch.State.RIGHT
        assert switch.state == Switch.State.RIGHT

    def test_invalid_state(self, switch):
        def bad_state():
            switch.state = "left"

        pytest.raises(ValueError, bad_state)

    def test_update(self, switch):
        switch.update({"state": "right"})
        assert switch.state == Switch.State.LEFT

    def test_subscription(self, switch):
        assert switch.add_subscriptions() == 0


class TestPlatform:
    """Tests for the platform object"""

    def test_track(self, souc, platform, track):
        souc.simulation_objects.append(track)
        souc.simulation_objects.append(platform)

        track.updater = souc
        platform.updater = souc

        assert platform.track == track

    def test_platform_id(self, platform):
        assert platform.platform_id == "fancy-city-platform-1"

    def test_update(self, platform):
        platform.update({})
        assert platform.platform_id == "fancy-city-platform-1"

    def test_subscription(self, platform):
        assert platform.add_subscriptions() == 0
