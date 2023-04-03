import marshmallow as marsh
from peewee import CharField

from src.base_model import BaseModel
class Token(BaseModel):
    """Represents a token."""

    class Schema(BaseModel.Schema):
        permission = marsh.fields.String(required=True)
        name = marsh.fields.String(required=True)
        hashedToken = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "Token":
            return Token(**data)

    permission = CharField()
    name = CharField()
    hashedToken = CharField()
