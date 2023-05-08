import pytest
from traci import edge

from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_types.track_speed_limit_fault import TrackSpeedLimitFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
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
    def track_speed_limit_fault_configuration(self, track: Track):
        return TrackSpeedLimitFaultConfiguration.create(
            **{
                "start_tick": 4,
                "end_tick": 130,
                "description": "test TrackSpeedLimitFault",
                "affected_element_id": track.identifier,
                "new_speed_limit": 60,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def track_speed_limit_fault(
        self,
        track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        logger: Logger,
        interlocking: IInterlockingDisruptor,
        simulation_object_updater: SimulationObjectUpdatingComponent,
    ):
        return TrackSpeedLimitFault(
            configuration=track_speed_limit_fault_configuration,
            logger=logger,
            simulation_object_updater=simulation_object_updater,
            interlocking=interlocking,
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
        track: Track,
        # the following arguments are needed fixtures
        # pylint: disable=unused-argument
        speed_update,
        combine_track_and_wrapper
        # pylint: enable=unused-argument
    ):
        track.max_speed = 100
        assert track.max_speed == 100
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.inject_fault(tick=tick)
        assert track.max_speed == track_speed_limit_fault.configuration.new_speed_limit

    def test_resolve_track_speed_limit_fault(
        self,
        tick,
        track_speed_limit_fault: TrackSpeedLimitFault,
        track: Track,
        # the following arguments are needed fixtures
        # pylint: disable=unused-argument
        speed_update,
        combine_track_and_wrapper,
        # pylint: enable=unused-argument
    ):
        track.max_speed = 100
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.inject_fault(tick=tick)
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.resolve_fault(tick=tick)
        assert track.max_speed == track_speed_limit_fault.old_speed_limit

    def test_resolve_element_does_not_exist(
        self,
        tick,
        empty_simulation_object_updater: SimulationObjectUpdatingComponent,
        track_speed_limit_fault: TrackSpeedLimitFault,
        track: Track
        # the following arguments are needed fixtures
        # pylint: disable=unused-argument
        speed_update,
        combine_track_and_wrapper,
        # pylint: enable=unused-argument
    ):
        track.max_speed = 100
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.inject_fault(tick)
        track_speed_limit_fault.simulation_object_updater = (
            empty_simulation_object_updater
        )
        with pytest.raises(ValueError):
            track_speed_limit_fault.resolve_fault(tick)
