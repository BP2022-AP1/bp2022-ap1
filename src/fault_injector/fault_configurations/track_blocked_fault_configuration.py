import marshmallow as marsh
from peewee import ForeignKeyField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


class TrackBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackBlockedFault class"""

    affected_element_id = TextField(null=False)

    def to_dict(self):
        data = super().to_dict()
        return {
            **data,
            "affected_element_id": self.affected_element_id,
        }


class TrackBlockedFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrackBlockedFaultConfiguration and SimulationConfiguration."""

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="track_blocked_fault_configuration_references",
    )
    track_blocked_fault_configuration = ForeignKeyField(
        TrackBlockedFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
