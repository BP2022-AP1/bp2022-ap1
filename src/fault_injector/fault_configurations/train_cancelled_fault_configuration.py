from src.fault_injector.fault_configurations.fault_configuration import FaultConfiguration
import marshmallow as marsh
from peewee import TextField

class TrainCancelledFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrainCancelledFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrainCancelledFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "TrainCancelledFaultConfiguration":
            return TrainCancelledFaultConfiguration(**data)

    affected_element_id = TextField()