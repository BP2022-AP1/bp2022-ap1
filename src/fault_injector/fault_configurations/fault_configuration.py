from abc import abstractmethod

import marshmallow as marsh
from peewee import FloatField, IntegerField, TextField

from src.base_model import BaseModel


class FaultConfiguration(BaseModel):
    """Class that contains the attributes of the Fault class"""

    class Schema(BaseModel.Schema):
        """Schema for the FaultConfiguration"""

        start_tick = marsh.fields.Integer(required=False)
        end_tick = marsh.fields.Integer(required=False)
        inject_probability = marsh.fields.Float(required=False)
        resolve_probability = marsh.fields.Float(required=False)
        description = marsh.fields.String()
        strategy = marsh.fields.String()

        @abstractmethod
        def _make(self, data: dict) -> "FaultConfiguration":
            raise NotImplementedError()

    start_tick = IntegerField(null=True)
    end_tick = IntegerField(null=True)
    inject_probability = FloatField(null=True)
    resolve_probability = FloatField(null=True)
    strategy = TextField()

    # - affected_element_ID: int = None // has to be implemented in subclasses
    description = TextField(default="injected Fault")
