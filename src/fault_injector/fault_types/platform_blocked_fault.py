import marshmallow as marsh
from peewee import TextField

from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfiguration


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

    def resolve_fault(self, component: Component):
        """resolve the PlatformBlockedFault that was previously injected into the given component

        :param component: The component the fault was injected into
        :type component: Component
        """
        # - get platform by id
        # - mark platform as no longer blocked
        raise NotImplementedError()


class PlatformBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the PlatformBlockedFault class"""

    class PlatformBlockedFaultConfigurationSchema(
        FaultConfiguration.FaultConfigurationSchema
    ):
        """Schema for PlatformBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

    affected_element_id = TextField()
