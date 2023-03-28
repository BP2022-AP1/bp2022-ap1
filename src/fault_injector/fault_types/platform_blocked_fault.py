from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfig


class PlatformBlockedFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self, component: Component):
        """inject PlatformBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get platform by id
        # - mark platform as blocked
        raise NotImplementedError()
    
class PlatformBlockedFaultConfig(FaultConfig):
    """Class that contains the attributes of the PlatformBlockedFault class"""

