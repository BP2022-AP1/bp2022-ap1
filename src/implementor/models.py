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
