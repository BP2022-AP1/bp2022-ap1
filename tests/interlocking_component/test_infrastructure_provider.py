from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.wrapper.simulation_objects import Edge, Signal, Switch, Train


class TestInfrastructurProvider:
    """This tests the InfrastructureProvieder."""

    def test_initialization(
        self, sumo_mock_infrastructure_provider: SumoInfrastructureProvider
    ):
        assert isinstance(sumo_mock_infrastructure_provider, SumoInfrastructureProvider)

    def test_turn_point(
        self,
        sumo_mock_infrastructure_provider: SumoInfrastructureProvider,
        yaramo_point,
    ):
        switch: Switch = None
        souc = (
            sumo_mock_infrastructure_provider.route_controller.simulation_object_updating_component
        )
        for potential_switch in souc.switches:
            if potential_switch.identifier == yaramo_point.point_id:
                switch = potential_switch
                break
        sumo_mock_infrastructure_provider.turn_point(yaramo_point, "right")
        assert switch.state == Switch.State.RIGHT
        sumo_mock_infrastructure_provider.turn_point(yaramo_point, "left")
        assert switch.state == Switch.State.LEFT

    def test_set_signal_state(
        self,
        sumo_mock_infrastructure_provider: SumoInfrastructureProvider,
        yaramo_signal,
        traffic_update,
    ):
        get_rr_count, get_gg_count = traffic_update
        rr_count = get_rr_count()  # Count for setting halt
        gg_count = get_gg_count()  # Count for setting go
        signal: Signal = None
        souc = (
            sumo_mock_infrastructure_provider.route_controller.simulation_object_updating_component
        )
        for potential_signal in souc.signals:
            if potential_signal.identifier == yaramo_signal.name:
                signal = potential_signal
                break
        sumo_mock_infrastructure_provider.set_signal_state(yaramo_signal, "go")
        assert signal.state == Signal.State.GO
        assert get_rr_count() == rr_count
        assert get_gg_count() == gg_count + 1
        assert sumo_mock_infrastructure_provider.event_bus.set_signal_go_count == 1
        assert sumo_mock_infrastructure_provider.event_bus.set_signal_halt_count == 0
        sumo_mock_infrastructure_provider.set_signal_state(yaramo_signal, "halt")
        assert signal.state == Signal.State.HALT
        assert get_rr_count() == rr_count + 1
        assert get_gg_count() == gg_count + 1
        assert sumo_mock_infrastructure_provider.event_bus.set_signal_go_count == 1
        assert sumo_mock_infrastructure_provider.event_bus.set_signal_halt_count == 1

    def test_train_drove_onto_track(
        self,
        interlocking_mock_infrastructure_provider: SumoInfrastructureProvider,
        sumo_train: Train,
        sumo_edge: Edge,
    ):
        interlocking_mock_infrastructure_provider.train_drove_onto_track(
            sumo_train, sumo_edge
        )
        assert (
            interlocking_mock_infrastructure_provider.route_controller.maybe_set_fahrstrasse_count
            == 1
        )
        interlocking = (
            interlocking_mock_infrastructure_provider.route_controller.interlocking
        )
        assert interlocking.tds_count_in_count == 1

    def test_train_drove_off_track(
        self,
        interlocking_mock_infrastructure_provider: SumoInfrastructureProvider,
        sumo_train: Train,
        sumo_edge: Edge,
    ):
        assert len(sumo_train.reserved_tracks) == 1
        assert len(sumo_edge.track.reservations) == 1
        interlocking_mock_infrastructure_provider.train_drove_off_track(
            sumo_train, sumo_edge
        )
        route_controller = interlocking_mock_infrastructure_provider.route_controller
        assert route_controller.maybe_free_fahrstrasse_count == 1
        assert route_controller.remove_reservation_count == 1
        interlocking = route_controller.interlocking
        assert interlocking.tds_count_out_count == 1
        assert len(sumo_train.reserved_tracks) == 0
        assert len(sumo_edge.track.reservations) == 0
