import marshmallow as marsh
from peewee import ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


class TrackSpeedLimitFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackSpeedLimitFault class"""

    affected_element_id = TextField()
    new_speed_limit = IntegerField(null=False)

    def to_dict(self):
        data = super().to_dict()
        return {
            **data,
            "affected_element_id": self.affected_element_id,
            "new_speed_limit": self.new_speed_limit,
        }


class TrackSpeedLimitFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrackSpeedLimitFaultConfiguration and SimulationConfiguration."""

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="track_speed_limit_fault_configuration_references",
    )
    track_speed_limit_fault_configuration = ForeignKeyField(
        TrackSpeedLimitFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
