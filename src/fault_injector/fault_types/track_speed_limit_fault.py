from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault, TrackMixIn
from src.wrapper.simulation_objects import Track


class TrackSpeedLimitFault(Fault, TrackMixIn):
    """A fault affecting the speed limit of tracks."""

    configuration: TrackSpeedLimitFaultConfiguration
    old_speed_limit: float
    track: Track

    def inject_fault(self, tick: int):
        """inject TrackSpeedLimitFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.track: Track = self.get_track(
            self.simulation_object_updater, self.configuration.affected_element_id
        )
        if self.track is None:
            raise ValueError("Track does not exist.")
        self.old_speed_limit = self.track.max_speed
        self.track.max_speed = self.configuration.new_speed_limit

        self.interlocking.insert_track_speed_limit_changed(self.track)
        self.logger.inject_track_speed_limit_fault(
            tick,
            self.configuration.id,
            self.track.identifier,
            self.old_speed_limit,
            self.configuration.new_speed_limit,
        )

    def resolve_fault(self, tick: int):
        """resolves the previously injected fault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        if self.track is None or self.track is not self.get_track(self.simulation_object_updater, self.track.identifier):
            raise ValueError("Track does not exist or fault not injected")

        self.track.max_speed = self.old_speed_limit
        self.interlocking.insert_track_speed_limit_changed(self.track)

        self.logger.resolve_track_speed_limit_fault(tick, self.configuration.id)
