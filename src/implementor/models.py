import marshmallow as marsh
from peewee import CharField

from src.base_model import BaseModel


class SimulationConfiguration(BaseModel):
    """Represents a single simulation configuration."""

    class Schema(BaseModel.Schema):
        description = marsh.fields.String()

        def _make(self, data: dict) -> "SimulationConfiguration":
            return SimulationConfiguration(**data)

    description = CharField(null=True)


class Run(BaseModel):
    """Represents the configuration of a single execution of a simulation configuration."""

    class Schema(BaseModel.Schema):
        def _make(self, data: dict) -> "Run":
            return Run(**data)
