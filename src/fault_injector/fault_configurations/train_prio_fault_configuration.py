import marshmallow as marsh
from peewee import ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


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


class TrainPrioFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrainPrioFaultConfiguration and SimulationConfiguration."""

    class Schema(BaseModel.Schema):
        """Marshmallow schema for TrainPrioFaultConfigurationXSimulationConfiguration"""

        simulation_configuration = marsh.fields.UUID(required=True)
        train_prio_fault_configuration = marsh.fields.UUID(required=True)

        def _make(
            self, data: dict
        ) -> "TrainPrioFaultConfigurationXSimulationConfiguration":
            """Constructs a TrainPrioFaultConfigurationXSimulationConfiguration from a dictionary.

            :param data: The dictionary.
            :return: A TrainPrioFaultConfigurationXSimulationConfiguration.
            """
            return TrainPrioFaultConfigurationXSimulationConfiguration(**data)

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="train_prio_fault_configuration_references",
    )
    train_prio_fault_configuration = ForeignKeyField(
        TrainPrioFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
