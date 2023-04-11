import marshmallow as marsh
from peewee import TextField

from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfiguration


class ScheduleBlockedFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self, component: Component):
        """inject ScheduleBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get schedule by id
        # - mark schedule as blocked
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        """resolves the previously injected ScheduleBlockedFault

        :param component: the component with the injected fault
        :type component: Component
        """
        raise NotImplementedError()


class ScheduleBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the ScheduleBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for ScheduleBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "ScheduleBlockedFaultConfiguration":
            return ScheduleBlockedFaultConfiguration(**data)

    affected_element_id = TextField()
