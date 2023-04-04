import pytest
from traci import trafficlight

from src.wrapper.simulation_objects import Signal


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
