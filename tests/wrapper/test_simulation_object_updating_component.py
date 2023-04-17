import pytest
from traci import trafficlight

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Platform, Signal, Switch, Track


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
        self.platform = Platform("fancy-platform")
        self.switch = Switch("fancy-switch")

        component = SimulationObjectUpdatingComponent()
        component.simulation_objects.append(self.signal)
        component.simulation_objects.append(self.track)
        component.simulation_objects.append(self.platform)
        component.simulation_objects.append(self.switch)

        return component

    @pytest.fixture
    def configured_component(self, traffic_update):
        # pylint: disable=unused-argument
        component = SimulationObjectUpdatingComponent(
            sumo_configuration="sumo-config/example.scenario.sumocfg"
        )
        return component

    def test_tracks(self, component):
        assert self.signal not in component.tracks
        assert self.track in component.tracks
        assert self.platform not in component.tracks
        assert self.switch not in component.tracks

    def test_signals(self, component):
        assert self.signal in component.signals
        assert self.track not in component.signals
        assert self.platform not in component.signals
        assert self.switch not in component.signals

    def test_platforms(self, component):
        assert self.signal not in component.platforms
        assert self.track not in component.platforms
        assert self.platform in component.platforms
        assert self.switch not in component.platforms

    def test_switches(self, component):
        assert self.signal not in component.switches
        assert self.track not in component.switches
        assert self.platform not in component.switches
        assert self.switch in component.switches

    def test_load(self, configured_component):
        # pylint: disable=unused-argument
        assert len(configured_component.signals) == 8
        assert len(configured_component.tracks) == 38
        assert len(configured_component.platforms) == 3
        assert len(configured_component.switches) == 4
