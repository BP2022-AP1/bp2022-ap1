from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class PlatformBlockedFault(Fault):
    """A fault that blocks a platform"""

    @classmethod
    def from_json(cls, json_object: str) -> "PlatformBlockedFault":
        """Constructs a PlatformBlockedFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a PlatformBlockFault
        :rtype: PlatformBlockedFault
        """
        raise NotImplementedError()

    def inject_fault(component: Component):
        """inject PlatformBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get platform by id
        # - mark platform as blocked
        raise NotImplementedError()