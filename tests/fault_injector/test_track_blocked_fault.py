import pytest

from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.track_blocked_fault import TrackBlockedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Track
from tests.decorators import recreate_db_setup


class TestTrackBlockedFault:
    """Tests for TrackBlockedFault"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def track_blocked_fault_configuration(self, basic_track: Track):
        return TrackBlockedFaultConfiguration.create(
            **{
                "start_time": 30,
                "end_time": 300,
                "description": "test TrackBlockedFault",
                "affected_element_id": basic_track.identifier,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def track_blocked_fault(
        self,
        track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
        event_bus: EventBus,
        souc: SimulationObjectUpdatingComponent,
        interlocking_disruptor: IInterlockingDisruptor,
    ):
        return TrackBlockedFault(
            configuration=track_blocked_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=souc,
            interlocking_disruptor=interlocking_disruptor,
        )

    def test_inject_track_blocked_fault(
        self,
        tick,
        track_blocked_fault: TrackBlockedFault,
        basic_track: Track,
    ):
        assert not basic_track.blocked
        track_blocked_fault.inject_fault(tick)
        assert (
            track_blocked_fault.interlocking_disruptor.route_controller.method_calls
            == 1
        )
        assert basic_track.blocked

    def test_resolve_track_blocked_fault(
        self,
        tick,
        track_blocked_fault: TrackBlockedFault,
        basic_track: Track,
    ):
        track_blocked_fault.inject_fault(tick)
        assert basic_track.blocked
        assert (
            track_blocked_fault.interlocking_disruptor.route_controller.method_calls
            == 1
        )
        track_blocked_fault.resolve_fault(tick)
        assert not basic_track.blocked
        assert (
            track_blocked_fault.interlocking_disruptor.route_controller.method_calls
            == 2
        )
