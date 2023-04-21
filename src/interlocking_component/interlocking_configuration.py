import marshmallow as marsh
from peewee import BooleanField, ForeignKeyField

from src.implementor.models import SimulationConfiguration

from src.base_model import BaseModel


class InterlockingConfiguration(BaseModel):
    """This class contains all fields needed to configure the Interlocking and RouteController"""

    class Schema(BaseModel.Schema):
        """Schema for the InterlockingConfiguration"""

        dynamicRouting = marsh.fields.Boolean()

        def _make(self, data: dict) -> "InterlockingConfiguration":
            return InterlockingConfiguration(**data)

    dynamicRouting = BooleanField(null=True)
    # null=True because this is not implemented yet


class InterlockingConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between InterlockingConfiguration and SimulationConfiguration."""

    class Schema(BaseModel.Schema):
        """Marshmallow schema for InterlockingConfigurationXSimulationConfiguration"""

        interlocking_configuration = marsh.fields.UUID(required=True)
        simulation_configuration = marsh.fields.UUID(required=True)

        def _make(
            self, data: dict
        ) -> "InterlockingConfigurationXSimulationConfiguration":
            """Constructs a InterlockingConfigurationXSimulationConfiguration from a dictionary.

            :param data: The dictionary.
            :return: A InterlockingConfigurationXSimulationConfiguration.
            """
            return InterlockingConfigurationXSimulationConfiguration(**data)

    spawner_configuration = ForeignKeyField(
        InterlockingConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="interlocking_configuration_references",
    )
