import pytest
from traci import trafficlight

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Signal, Switch


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
    def component(self, traffic_update) -> SimulationObjectUpdatingComponent:
        # pylint: disable=unused-argument,attribute-defined-outside-init

        self.signal = Signal("fancy-signal")
        self.edge = Edge("fancy-edge")
        self.platform = Platform("fancy-platform")
        self.switch = Switch("fancy-switch")

        component = SimulationObjectUpdatingComponent()
        component.simulation_objects.append(self.signal)
        component.simulation_objects.append(self.edge)
        component.simulation_objects.append(self.platform)
        component.simulation_objects.append(self.switch)

        return component

    @pytest.fixture
    def configured_component(self, traffic_update) -> SimulationObjectUpdatingComponent:
        # pylint: disable=unused-argument
        component = SimulationObjectUpdatingComponent(
            sumo_configuration="sumo-config/example.scenario.sumocfg"
        )
        return component

    def test_tracks(self, component: SimulationObjectUpdatingComponent):
        assert self.signal not in component.edges
        assert self.edge in component.edges
        assert self.platform not in component.edges
        assert self.switch not in component.edges

    def test_signals(self, component: SimulationObjectUpdatingComponent):
        assert self.signal in component.signals
        assert self.edge not in component.signals
        assert self.platform not in component.signals
        assert self.switch not in component.signals

    def test_platforms(self, component: SimulationObjectUpdatingComponent):
        assert self.signal not in component.platforms
        assert self.edge not in component.platforms
        assert self.platform in component.platforms
        assert self.switch not in component.platforms

    def test_switches(self, component: SimulationObjectUpdatingComponent):
        assert self.signal not in component.switches
        assert self.edge not in component.switches
        assert self.platform not in component.switches
        assert self.switch in component.switches

    def test_load(self, configured_component: SimulationObjectUpdatingComponent):
        assert len(configured_component.signals) == 8
        assert len(configured_component.edges) == 38
        assert len(configured_component.platforms) == 3
        assert len(configured_component.switches) == 4
        assert len(configured_component.tracks) == 19

        for node in configured_component.switches:
            assert len(node.edges) == 3

        for node in configured_component.signals:
            assert 1 <= len(node.edges) <= 2
