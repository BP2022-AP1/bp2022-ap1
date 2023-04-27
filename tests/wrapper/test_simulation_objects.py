import os
from uuid import uuid4

import pytest
from traci import constants, edge, trafficlight, vehicle

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Signal, Switch, Track, Train


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


class TestEdge:
    """Tests for the edge component"""

    def test_update_speed(self, edge1, speed_update):
        # pylint: disable=unused-argument
        edge1.max_speed = 100

        assert edge1.max_speed == 100

    def test_default_blocked(self, edge1):
        assert not edge1.blocked

    def test_update_blocked(self, edge1):
        edge1.blocked = True

        assert edge1.blocked


class TestTrack:
    """Tests the track component"""

    def test_update_speed(self, track, speed_update):
        # pylint: disable=unused-argument

        track.max_speed = (100, 200)
        assert track.edges[0].max_speed == 100
        assert track.edges[1].max_speed == 200
        assert track.max_speed == (100, 200)

        track.max_speed = 150
        assert track.edges[0].max_speed == 150
        assert track.edges[1].max_speed == 150
        assert track.max_speed == 150

    def test_blocked(self, track):
        track.blocked = (True, False)
        assert track.edges[0].blocked
        assert not track.edges[1].blocked
        assert track.blocked == (True, False)

        track.blocked = True
        assert track.edges[0].blocked
        assert track.edges[1].blocked
        assert track.blocked


class TestTrain:
    """Tests for the train object"""

    def test_edge(self, train, souc, edge1):
        souc.simulation_objects.append(train)
        souc.simulation_objects.append(edge1)

        train.updater = souc
        edge1.updater = souc

        assert train.edge.identifier == edge1.identifier

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

    def test_update(self, souc, train, edge2):
        train.updater = souc
        edge2.updater = souc

        souc.simulation_objects.append(train)
        souc.simulation_objects.append(edge2)

        train.update(
            {
                constants.VAR_POSITION: (
                    110,
                    90,
                ),
                constants.VAR_ROAD_ID: "cfc57-1",
                constants.VAR_ROUTE: "ending-route",
                constants.VAR_SPEED: 10,
            }
        )
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

    def test_edge(self, souc, platform, edge1):
        souc.simulation_objects.append(edge1)
        souc.simulation_objects.append(platform)

        edge1.updater = souc
        platform.updater = souc

        assert platform.edge == edge1

    def test_platform_id(self, platform):
        assert platform.platform_id == "fancy-city-platform-1"

    def test_update(self, platform):
        platform.update({})
        assert platform.platform_id == "fancy-city-platform-1"

    def test_subscription(self, platform):
        assert platform.add_subscriptions() == 0
