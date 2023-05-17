from peewee import BooleanField, ForeignKeyField

from src.base_model import BaseModel, SerializableBaseModel
from src.implementor.models import SimulationConfiguration


class InterlockingConfiguration(SerializableBaseModel):
    """This class contains all fields needed to configure the Interlocking and RouteController"""

    dynamicRouting = BooleanField(null=True)
    # null=True because this is not implemented yet

    def to_dict(self):
        data = super().to_dict()
        return {"dynamicRouting": self.dynamicRouting, **data}


class InterlockingConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between InterlockingConfiguration and SimulationConfiguration."""

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="interlocking_configuration_references",
    )
    interlocking_configuration = ForeignKeyField(
        InterlockingConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
