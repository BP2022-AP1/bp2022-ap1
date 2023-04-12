import marshmallow as marsh
from peewee import TextField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)


class TrackBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrackBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "TrackBlockedFaultConfiguration":
            return TrackBlockedFaultConfiguration(**data)

    affected_element_id = TextField()
