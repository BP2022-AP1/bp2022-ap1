from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrackBlockedFault(Fault):
    """A fault that blocks a track"""

    @classmethod
    def from_json(cls, json_object: str) -> "TrackBlockedFault":
        """Constructs a TrackBlockedFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a TrackBlockFault
        :rtype: TrackBlockedFault
        """
        raise NotImplementedError()

    def inject_fault(component: Component):
        """inject TrackBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get track by id
        # - mark track as blocked
        raise NotImplementedError()
