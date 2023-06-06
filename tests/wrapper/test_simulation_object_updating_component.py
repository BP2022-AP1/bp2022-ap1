import pytest
from traci import trafficlight

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Signal, Switch, Train


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

    def test_load(self, configured_souc: SimulationObjectUpdatingComponent):
        assert len(configured_souc.signals) == 8
        assert len(configured_souc.edges) == 32
        assert len(configured_souc.platforms) == 4
        assert len(configured_souc.switches) == 4
        assert len(configured_souc.tracks) == 16

        for node in configured_souc.switches:
            assert len(node.edges) == 6

        for node in configured_souc.signals:
            assert 1 <= len(node.edges) <= 4

    def test_edge_refs(self, configured_souc: SimulationObjectUpdatingComponent):
        for edge in configured_souc.edges:
            assert edge.from_node is not None
            assert edge.to_node is not None

            assert edge in edge.from_node.edges

    def test_node_refs(self, configured_souc: SimulationObjectUpdatingComponent):
        for node in configured_souc.nodes:
            assert len(node.edges) >= 1

            for edge in node.edges:
                if node not in (edge.to_node, edge.from_node):
                    print(
                        node.identifier,
                        edge.to_node.identifier,
                        edge.from_node.identifier,
                    )
                    print(
                        node.identifier == edge.to_node.identifier,
                        edge.to_node.identifier == edge.from_node.identifier,
                    )

                    assert node in (edge.to_node, edge.from_node)

    def test_stale_train_is_removed(
        self,
        configured_souc: SimulationObjectUpdatingComponent,
        train: Train,
        results,
        all_trains,
    ):
        # pylint: disable=unused-argument
        configured_souc.simulation_objects.append(train)
        configured_souc.next_tick(1)
        configured_souc.next_tick(2)

        assert len(configured_souc.trains) == 0
