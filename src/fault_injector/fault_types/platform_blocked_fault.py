import marshmallow as marsh
from peewee import TextField

from src.fault_injector.fault_types.fault import Fault, FaultConfiguration


class PlatformBlockedFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self):
        """inject PlatformBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get platform by id
        # - mark platform as blocked
        raise NotImplementedError()

    def resolve_fault(self):
        """resolve the PlatformBlockedFault that was previously injected into the given component

        :param component: The component the fault was injected into
        :type component: Component
        """
        # - get platform by id
        # - mark platform as no longer blocked
        raise NotImplementedError()


class PlatformBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the PlatformBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for PlatformBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "PlatformBlockedFaultConfiguration":
            return PlatformBlockedFaultConfiguration(**data)

    affected_element_id = TextField(null=False)
