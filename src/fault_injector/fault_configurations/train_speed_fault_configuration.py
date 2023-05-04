import marshmallow as marsh
from peewee import FloatField, ForeignKeyField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


class TrainSpeedFaultConfiguration(FaultConfiguration):
    """Class that contains the configuration attributes of the TrainSpeedFault class"""

    affected_element_id = TextField(null=False)
    new_speed = FloatField(null=False)

    def to_dict(self):
        data = super().to_dict()
        return {
            **data,
            "affected_element_id": self.affected_element_id,
            "new_speed": self.new_speed,
        }


class TrainSpeedFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrainSpeedFaultConfiguration and SimulationConfiguration."""

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="train_speed_fault_configuration_references",
    )
    train_speed_fault_configuration = ForeignKeyField(
        TrainSpeedFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
