import marshmallow as marsh
from peewee import CharField

from src.base_model import BaseModel


class Run(BaseModel):
    """Represents the configuration of a single execution of a simulation configuration."""

    class Schema(BaseModel.Schema):
        def _make(self, data: dict) -> "Run":
            return Run(**data)

