import marshmallow as marsh
from peewee import IntegerField, TextField

from src.base_model import BaseModel


class FaultConfiguration(BaseModel):
    """Class that contains the attributes of the Fault class"""

    class Schema(BaseModel.Schema):
        """Schema for the FaultConfiguration"""

        start_tick = marsh.fields.Integer(required=True)
        end_tick = marsh.fields.Integer(required=True)
        description = marsh.fields.String()

        def _make(self, data: dict) -> "FaultConfiguration":
            return FaultConfiguration(**data)

    start_tick = IntegerField(null=False)
    end_tick = IntegerField(null=False)

    # - affected_element_ID: int = None // has to be implemented in subclasses
    description = TextField(default="injected Fault")
