from peewee import ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


class TrainPrioFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrainPrioFault class"""

    affected_element_id = TextField()
    new_prio = IntegerField(null=False)

    def to_dict(self):
        """Serializes TrainPrioFaultConfiguration objects"""

        data = super().to_dict()
        return {
            **data,
            "affected_element_id": self.affected_element_id,
            "new_prio": self.new_prio,
        }


class TrainPrioFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrainPrioFaultConfiguration and SimulationConfiguration."""

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
