import marshmallow as marsh
from peewee import CharField, ForeignKeyField

from src.base_model import BaseModel


class Token(BaseModel):
    """Represents a token."""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for the token model."""

        permission = marsh.fields.String(required=True)
        name = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "Token":
            return Token(**data)

    permission = CharField()
    name = CharField()
    hashedToken = CharField()


class SimulationConfiguration(BaseModel):
    """Represents a single simulation configuration."""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for the simulation configuration model."""

        description = marsh.fields.String()
        token = marsh.fields.UUID(required=True)

        def _make(self, data: dict) -> "SimulationConfiguration":
            return SimulationConfiguration(**data)

    description = CharField(null=True)
    token = ForeignKeyField(Token, backref="simulation_configurations")


class Run(BaseModel):
    """Represents the configuration of a single execution of a simulation configuration."""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for the run model."""

        def _make(self, data: dict) -> "Run":
            return Run(**data)

        simulation_configuration = marsh.fields.UUID(required=True)

    simulation_configuration = ForeignKeyField(SimulationConfiguration, backref="runs")
