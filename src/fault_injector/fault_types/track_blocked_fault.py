from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfig


class TrackBlockedFault(Fault):
    """A fault that blocks a track"""

    def inject_fault(self, component: Component):
        """inject TrackBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get track by id
        # - mark track as blocked
        raise NotImplementedError()

class TrackBlockedFaultConfig(FaultConfig):
    """Class that contains the attributes of the TrackBlockedFault class"""