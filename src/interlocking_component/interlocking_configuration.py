import marshmallow as marsh
from peewee import BooleanField, ForeignKeyField

from src.base_model import BaseModel, SerializableBaseModel
from src.implementor.models import SimulationConfiguration


class InterlockingConfiguration(SerializableBaseModel):
    """This class contains all fields needed to configure the Interlocking and RouteController"""

    class Schema(SerializableBaseModel.Schema):
        """Schema for the InterlockingConfiguration"""

        dynamicRouting = marsh.fields.Boolean()

        def _make(self, data: dict) -> "InterlockingConfiguration":
            return InterlockingConfiguration(**data)

    dynamicRouting = BooleanField(null=True)
    # null=True because this is not implemented yet


class InterlockingConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between InterlockingConfiguration and SimulationConfiguration."""

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="interlocking_configuration_references",
    )
    spawner_configuration = ForeignKeyField(
        InterlockingConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
