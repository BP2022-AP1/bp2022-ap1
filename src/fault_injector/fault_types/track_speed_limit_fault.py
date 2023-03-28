from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfig


class TrackSpeedLimitFault(Fault):
    """A fault affecting the speed limit of tracks."""

    def inject_fault(self, component: Component):
        """inject TrackSpeedLimitFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get track object
        # - save the current speed limit of the track in old_speed_limit
        # - set track speed limit to new_speed_limit
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        # - get track object
        # - set the track speed limit to old_speed_limit

        raise NotImplementedError()


class TrackSpeedLimitFaultConfig(FaultConfig):
    """Class that contains the attributes of the TrackSpeedLimitFaultFault class"""

    new_speed_limit: int = None
    old_speed_limit: int = None
