import abc
import os
from uuid import uuid4

import marshmallow as marsh
from peewee import Model, PostgresqlDatabase, SqliteDatabase, UUIDField

db: PostgresqlDatabase = PostgresqlDatabase(
    database=os.getenv("DATABASE_NAME") or "postgres",
    user=os.getenv("DATABASE_USER") or "postgres",
    password=os.getenv("DATABASE_PASSWORD") or "root",
    host=os.getenv("DATABASE_HOST") or "localhost",
    port=os.getenv("DATABASE_PORT") or 5432,
)


class BaseModel(Model):
    """All model classes have to inherit from this base class."""

    class Meta:
        """Set Database"""

        database: SqliteDatabase = db

    class Schema(marsh.Schema):
        """The marshmallow schema all model schemas have to inherit from."""

        id = marsh.fields.UUID()

        @abc.abstractmethod
        def _make(self, data: dict) -> "BaseModel":
            """Constructs a model object from a dictionary."""
            raise NotImplementedError()

        @marsh.post_load
        def make(self, data: dict, **_) -> "BaseModel":
            """Constructs a model object from a dictionary."""
            return self._make(data)

    id = UUIDField(primary_key=True, default=uuid4)

    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        """constructs a model object from a dictionary.

        :param data: the dictionary
        :return: an instance of the model
        """
        return cls.Schema().load(data)

    def to_dict(self) -> dict:
        """serializes the model object to a dictionary.

        :return: the dictionary
        """
        return self.Schema().dump(self)
