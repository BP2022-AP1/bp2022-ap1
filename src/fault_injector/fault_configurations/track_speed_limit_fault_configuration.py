import marshmallow as marsh
from peewee import ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


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
