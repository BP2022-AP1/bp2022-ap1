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
    def track_blocked_fault_configuration(self, track: Track):
        return TrackBlockedFaultConfiguration.create(
            **{
                "start_tick": 30,
                "end_tick": 300,
                "description": "test TrackBlockedFault",
                "affected_element_id": track.identifier,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def track_blocked_fault(
        self,
        track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
        event_bus: EventBus,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        return TrackBlockedFault(
            configuration=track_blocked_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=simulation_object_updater,
            interlocking=interlocking,
        )

    def test_inject_track_blocked_fault(
        self,
        tick,
        track_blocked_fault: TrackBlockedFault,
        track: Track,
        # the following argument is a needed fixture
        # pylint: disable-next=unused-argument
        combine_track_and_wrapper,
    ):
        assert not track.blocked
        with pytest.raises(NotImplementedError):
            track_blocked_fault.inject_fault(tick)
        assert track.blocked

    def test_resolve_track_blocked_fault(
        self,
        tick,
        track_blocked_fault: TrackBlockedFault,
        track: Track,
        # the following argument is a needed fixture
        # pylint: disable-next=unused-argument
        combine_track_and_wrapper,
    ):
        with pytest.raises(NotImplementedError):
            track_blocked_fault.inject_fault(tick)
        assert track.blocked
        with pytest.raises(NotImplementedError):
            track_blocked_fault.resolve_fault(tick)
        assert not track.blocked
