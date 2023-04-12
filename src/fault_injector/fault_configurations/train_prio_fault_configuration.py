import marshmallow as marsh
from peewee import IntegerField, TextField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)


class TrainPrioFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrainPrioFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrainPrioFaultConfiguration"""

        affected_element_id = marsh.fields.String()
        new_prio = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrainPrioFaultConfiguration":
            return TrainPrioFaultConfiguration(**data)

    affected_element_id = TextField()
    new_prio = IntegerField(null=False)
