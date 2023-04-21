import marshmallow as marsh
from peewee import FloatField, TextField, ForeignKeyField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.base_model import BaseModel
from src.implementor.models import SimulationConfiguration


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


class TrainSpeedFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrainSpeedFaultConfiguration and SimulationConfiguration."""

    class Schema(BaseModel.Schema):
        """Marshmallow schema for TrainSpeedFaultConfigurationXSimulationConfiguration"""

        train_speed_fault_configuration = marsh.fields.UUID(required=True)
        simulation_configuration = marsh.fields.UUID(required=True)

        def _make(
            self, data: dict
        ) -> "TrainSpeedFaultConfigurationXSimulationConfiguration":
            """Constructs a TrainSpeedFaultConfigurationXSimulationConfiguration from a dictionary.

            :param data: The dictionary.
            :return: A TrainSpeedFaultConfigurationXSimulationConfiguration.
            """
            return TrainSpeedFaultConfigurationXSimulationConfiguration(**data)

    train_speed_fault_configuration = ForeignKeyField(
        TrainSpeedFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="train_speed_fault_configuration_references",
    )
