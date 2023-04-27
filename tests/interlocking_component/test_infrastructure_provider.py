import pytest

from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.wrapper.simulation_objects import Signal, Switch


class TestInfrastructurProvider:
    def test_initialization(self, infrastructure_provider: SumoInfrastructureProvider):
        assert isinstance(infrastructure_provider, SumoInfrastructureProvider)

    def test_turn_point(
        self, infrastructure_provider: SumoInfrastructureProvider, yaramo_point
    ):
        switch: Switch = None
        for (
            potencial_switch
        ) in (
            infrastructure_provider.route_controller.simulation_object_updating_component.switches
        ):
            if potencial_switch.identifier == yaramo_point.point_id:
                switch = potencial_switch
                break
        infrastructure_provider.turn_point(yaramo_point, "right")
        assert switch.state == Switch.State.RIGHT
        infrastructure_provider.turn_point(yaramo_point, "left")
        assert switch.state == Switch.State.LEFT

    def test_set_signal_state(
        self,
        infrastructure_provider: SumoInfrastructureProvider,
        yaramo_signal,
        traffic_update,
    ):
        get_rr_count, get_gg_count = traffic_update
        rr_count = get_rr_count()  # Count for setting halt
        gg_count = get_gg_count()  # Count for setting go
        signal: Signal = None
        for (
            potencial_signal
        ) in (
            infrastructure_provider.route_controller.simulation_object_updating_component.signals
        ):
            if potencial_signal.identifier == yaramo_signal.name:
                signal = potencial_signal
                break
        infrastructure_provider.set_signal_state(yaramo_signal, "go")
        assert signal.state == Signal.State.GO
        assert get_rr_count() == rr_count
        assert get_gg_count() == gg_count + 1
        infrastructure_provider.set_signal_state(yaramo_signal, "halt")
        assert signal.state == Signal.State.HALT
        assert get_rr_count() == rr_count + 1
        assert get_gg_count() == gg_count + 1
