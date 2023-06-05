from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault, TrackMixIn
from src.wrapper.simulation_objects import Track


class TrackBlockedFault(Fault, TrackMixIn):
    """A fault that blocks a track"""

    configuration: TrackBlockedFaultConfiguration
    track: Track = None

    def inject_fault(self, tick: int):
        """inject TrackBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.track: Track = self.get_track(
            self.simulation_object_updater, self.configuration.affected_element_id
        )
        self.track.blocked = True

        self.interlocking_disruptor.insert_track_blocked(self.track)
        self.event_bus.inject_track_blocked_fault(
            tick, self.configuration.id, self.track.identifier
        )

    def resolve_fault(self, tick: int):
        """resolves the previously injected fault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        if self.track is None:
            raise ValueError("TrackBlockedFault not injected")

        self.track.blocked = False
        self.interlocking_disruptor.insert_track_unblocked(self.track)

        self.event_bus.resolve_track_blocked_fault(tick, self.configuration.id)
