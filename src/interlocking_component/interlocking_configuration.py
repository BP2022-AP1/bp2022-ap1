import marshmallow as marsh
from peewee import BooleanField

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
