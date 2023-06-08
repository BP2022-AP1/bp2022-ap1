import pytest
from traci import edge

from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_types.track_speed_limit_fault import TrackSpeedLimitFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Track
from tests.decorators import recreate_db_setup


class TestTrackSpeedLimitFault:
    """Tests for TrackSpeedLimitFault"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def track_speed_limit_fault_configuration(self, basic_track: Track):
        return TrackSpeedLimitFaultConfiguration.create(
            **{
                "start_tick": 4,
                "end_tick": 130,
                "description": "test TrackSpeedLimitFault",
                "affected_element_id": basic_track.identifier,
                "new_speed_limit": 60,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def track_speed_limit_fault(
        self,
        track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        event_bus: EventBus,
        interlocking_disruptor: IInterlockingDisruptor,
        souc: SimulationObjectUpdatingComponent,
    ):
        return TrackSpeedLimitFault(
            configuration=track_speed_limit_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=souc,
            interlocking_disruptor=interlocking_disruptor,
        )

    @pytest.fixture
    def speed_update(self, monkeypatch):
        def set_max_speed(identifier: str, speed: float) -> None:
            # pylint: disable=unused-argument
            pass

        monkeypatch.setattr(edge, "setMaxSpeed", set_max_speed)

    def test_inject_track_speed_limit_fault(
        self,
        tick,
        track_speed_limit_fault: TrackSpeedLimitFault,
        basic_track: Track,
    ):
        basic_track.max_speed = 100
        assert basic_track.max_speed == 100
        track_speed_limit_fault.inject_fault(tick=tick)
        assert (
            basic_track.max_speed
            == track_speed_limit_fault.configuration.new_speed_limit
        )
        # assert (
        #     track_speed_limit_fault.interlocking_disruptor.route_controller.method_calls
        #     == 1
        # )

    def test_resolve_track_speed_limit_fault(
        self, tick, track_speed_limit_fault: TrackSpeedLimitFault, basic_track: Track
    ):
        basic_track.max_speed = 100
        track_speed_limit_fault.inject_fault(tick=tick)
        # assert (
        #     track_speed_limit_fault.interlocking_disruptor.route_controller.method_calls
        #     == 1
        # )
        track_speed_limit_fault.resolve_fault(tick=tick)
        assert basic_track.max_speed == track_speed_limit_fault.old_speed_limit
        # assert (
        #     track_speed_limit_fault.interlocking_disruptor.route_controller.method_calls
        #     == 2
        # )
