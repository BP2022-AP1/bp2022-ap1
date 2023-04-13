import pytest
from traci import edge

from src.fault_injector.fault_types.track_speed_limit_fault import (
    TrackSpeedLimitFault,
    TrackSpeedLimitFaultConfiguration,
)
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
    def logger(self, run):
        return Logger(run.id)

    @pytest.fixture
    def interlocking(self):
        return IInterlockingDisruptor()

    @pytest.fixture
    def track(self) -> Track:
        return Track("fault injector track")

    @pytest.fixture
    def wrapper(self):
        return SimulationObjectUpdatingComponent()

    @pytest.fixture
    def combine(self, track, wrapper):
        track.updater = wrapper
        wrapper.simulation_objects.append(track)
        return (track, wrapper)

    @pytest.fixture
    def track_speed_limit_fault_configuration(self, track: Track):
        return TrackSpeedLimitFaultConfiguration.create(
            **{
                "start_tick": 4,
                "end_tick": 130,
                "description": "test TrackSpeedLimitFault",
                "affected_element_id": track.identifier,
                "new_speed_limit": 60,
            }
        )

    @pytest.fixture
    def track_speed_limit_fault(
        self,
        track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        logger: Logger,
        interlocking: IInterlockingDisruptor,
        wrapper: SimulationObjectUpdatingComponent,
    ):
        return TrackSpeedLimitFault(
            configuration=track_speed_limit_fault_configuration,
            logger=logger,
            wrapper=wrapper,
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
        combine,
        track_speed_limit_fault: TrackSpeedLimitFault,
        track: Track,
        speed_update,
    ):
        # pylint: disable=unused-argument
        track.max_speed = 100
        assert track.max_speed == 100
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.inject_fault()
        # comment in following line if `insert_track_speed_limit_changed`
        # in RouteController is implemented
        # assert track.max_speed == track_speed_limit_fault.configuration.new_speed_limit

    def test_resolve_track_speed_limit_fault(
        self,
        combine,
        track_speed_limit_fault: TrackSpeedLimitFault,
        track: Track,
        speed_update,
    ):
        # pylint: disable=unused-argument
        track.max_speed = 100
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.inject_fault()
        with pytest.raises(NotImplementedError):
            track_speed_limit_fault.resolve_fault()
        # assert track.max_speed == track_speed_limit_fault.old_speed_limit
