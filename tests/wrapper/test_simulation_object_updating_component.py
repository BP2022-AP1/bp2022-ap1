import pytest
from traci import trafficlight

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Signal, Track


class TestSimulationObjectUpdatingComponent:
    """Tests for the SimulationObjectUpdatingComponent"""

    @pytest.fixture
    def traffic_update(self, monkeypatch):
        def set_traffic_light_state(identifier: str, state: str) -> None:
            # pylint: disable=unused-argument
            pass  # we don't care what happens here

        monkeypatch.setattr(
            trafficlight, "setRedYellowGreenState", set_traffic_light_state
        )

    @pytest.fixture
    def component(self, traffic_update):
        # pylint: disable=unused-argument,attribute-defined-outside-init

        self.signal = Signal("fancy-signal")
        self.track = Track("fancy-track")

        component = SimulationObjectUpdatingComponent()
        component.simulation_objects.append(self.signal)
        component.simulation_objects.append(self.track)

        return component

    def test_tracks(self, component):
        assert self.signal not in component.tracks
        assert self.track in component.tracks

    def test_signals(self, component):
        assert self.signal in component.signals
        assert self.track not in component.signals
