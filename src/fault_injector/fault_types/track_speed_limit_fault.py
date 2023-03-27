from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrackSpeedLimitFault(Fault):
    """A fault affecting the speed limit of tracks."""

    new_speed_limit: int = None
    old_speed_limit: int = None

    @classmethod
    def from_json(cls, json_object: str) -> "TrackSpeedLimitFault":
        """Constructs a TrackSpeedLimitFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a TrackSpeedLimitFault
        :rtype: TrackSpeedLimitFault
        """
        raise NotImplementedError()

    def inject_fault(component: Component):
        """inject TrackSpeedLimitFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get track object
        # - save the current speed limit of the track in old_speed_limit
        # - set track speed limit to new_speed_limit
        raise NotImplementedError()

    def resolve_fault(component: Component):
        # - get track object
        # - set the track speed limit to old_speed_limit

        raise NotImplementedError()
