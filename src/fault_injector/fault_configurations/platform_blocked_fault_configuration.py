from src.fault_injector.fault_configurations.fault_configuration import FaultConfiguration
import marshmallow as marsh
from peewee import TextField

class PlatformBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the PlatformBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for PlatformBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "PlatformBlockedFaultConfiguration":
            return PlatformBlockedFaultConfiguration(**data)

    affected_element_id = TextField(null=False)