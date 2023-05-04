import marshmallow as marsh
from peewee import ForeignKeyField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


class PlatformBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the PlatformBlockedFault class"""

    affected_element_id = TextField(null=False)

    def to_dict(self):
        data = super().to_dict()
        return {
            **data,
            "affected_element_id": self.affected_element_id,
        }


class PlatformBlockedFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between PlatformBlockedFaultConfiguration and SimulationConfiguration."""

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="platform_blocked_fault_configuration_references",
    )
    platform_blocked_fault_configuration = ForeignKeyField(
        PlatformBlockedFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
