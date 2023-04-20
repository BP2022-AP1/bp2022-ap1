from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.wrapper.simulation_objects import Track


class TrackBlockedFault(Fault):
    """A fault that blocks a track"""

    configuration: TrackBlockedFaultConfiguration
    track: Track

    def inject_fault(self, tick: int):
        """inject TrackBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # pylint: disable-next=duplicate-code
        self.track: Track = [
            track
            for track in self.wrapper.tracks
            if track.identifier == self.configuration.affected_element_id
        ][0]
        self.track.blocked = True

        self.interlocking.insert_track_blocked(self.track.identifier)
        self.logger.inject_track_blocked_fault(
            tick, self.configuration.id, self.track.identifier
        )

    def resolve_fault(self, tick: int):
        """resolves the previously injected fault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        if self.track is None:
            raise ValueError("Track not set, probably due to not injecting the fault")

        self.track.blocked = False
        self.interlocking.insert_track_unblocked(self.track.identifier)

        self.logger.resolve_track_blocked_fault(tick, self.configuration.id)
