from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.wrapper.simulation_objects import Track


class TrackSpeedLimitFault(Fault):
    """A fault affecting the speed limit of tracks."""

    configuration: TrackSpeedLimitFaultConfiguration
    old_speed_limit: float
    track: Track

    def inject_fault(self, tick: int):
        """inject TrackSpeedLimitFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.track: Track = [
            track
            for track in self.wrapper.tracks
            if track.identifier == self.configuration.affected_element_id
        ][0]
        self.old_speed_limit = self.track.max_speed
        self.track.max_speed = self.configuration.new_speed_limit

        self.interlocking.insert_track_speed_limit_changed(self.track.identifier)
        self.logger.inject_track_speed_limit_fault(
            tick,
            self.configuration.id,
            self.track.identifier,
            self.old_speed_limit,
            self.configuration.new_speed_limit,
        )

        # - get track object
        # - save the current speed limit of the track in old_speed_limit
        # - set track speed limit to new_speed_limit

    def resolve_fault(self, tick: int):
        """resolves the previously injected fault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        self.track.max_speed = self.old_speed_limit
        self.interlocking.insert_track_speed_limit_changed(self.track.identifier)

        self.logger.resolve_track_speed_limit_fault(tick, self.configuration.id)

        # - get track object
        # - set the track speed limit to old_speed_limit
