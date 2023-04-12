import marshmallow as marsh
from peewee import IntegerField, TextField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)


class TrackSpeedLimitFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackSpeedLimitFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrackSpeedLimitFaultConfiguration"""

        affected_element_id = marsh.fields.String()
        new_speed_limit = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrackSpeedLimitFaultConfiguration":
            return TrackSpeedLimitFaultConfiguration(**data)

    affected_element_id = TextField()
    new_speed_limit = IntegerField(null=False)
