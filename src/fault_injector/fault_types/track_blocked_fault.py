import marshmallow as marsh
from peewee import TextField

from src.fault_injector.fault_types.fault import Fault, FaultConfiguration


class TrackBlockedFault(Fault):
    """A fault that blocks a track"""

    def inject_fault(self):
        """inject TrackBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get track by id
        # - mark track as blocked
        raise NotImplementedError()

    def resolve_fault(self):
        """resolves the previously injected fault

        :param component: the component with the injected TrackBlockedFault
        :type component: Component
        """
        # - get track by id
        # - mark track as no longer blocked
        raise NotImplementedError()


class TrackBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrackBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "TrackBlockedFaultConfiguration":
            return TrackBlockedFaultConfiguration(**data)

    affected_element_id = TextField()
