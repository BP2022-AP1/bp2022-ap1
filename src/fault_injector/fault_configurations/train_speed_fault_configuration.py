import marshmallow as marsh
from peewee import FloatField, TextField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)


class TrainSpeedFaultConfiguration(FaultConfiguration):
    """Class that contains the configuration attributes of the TrainSpeedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrainSpeedFaultConfiguration"""

        affected_element_id = marsh.fields.String(required=True)
        new_speed = marsh.fields.Float(required=True)

        def _make(self, data: dict) -> "TrainSpeedFaultConfiguration":
            return TrainSpeedFaultConfiguration(**data)

    affected_element_id = TextField(null=False)
    new_speed = FloatField(null=False)
