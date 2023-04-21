import marshmallow as marsh
from peewee import TextField, ForeignKeyField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.base_model import BaseModel
from src.implementor.models import SimulationConfiguration


class TrackBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrackBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "TrackBlockedFaultConfiguration":
            return TrackBlockedFaultConfiguration(**data)

    affected_element_id = TextField()


class TrackBlockedFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between TrackBlockedFaultConfiguration and SimulationConfiguration."""

    class Schema(BaseModel.Schema):
        """Marshmallow schema for TrackBlockedFaultConfigurationXSimulationConfiguration"""

        track_blocked_fault_configuration = marsh.fields.UUID(required=True)
        simulation_configuration = marsh.fields.UUID(required=True)

        def _make(
            self, data: dict
        ) -> "TrackBlockedFaultConfigurationXSimulationConfiguration":
            """Constructs a TrackBlockedFaultConfigurationXSimulationConfiguration from a dictionary.

            :param data: The dictionary.
            :return: A TrackBlockedFaultConfigurationXSimulationConfiguration.
            """
            return TrackBlockedFaultConfigurationXSimulationConfiguration(**data)

    track_blocked_fault_configuration = ForeignKeyField(
        TrackBlockedFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="track_blocked_fault_configuration_references",
    )
