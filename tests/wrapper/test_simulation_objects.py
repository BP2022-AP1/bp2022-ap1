import pytest
from traci import trafficlight, edge

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