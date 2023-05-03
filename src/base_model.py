import abc
import os
from datetime import datetime
from uuid import uuid4

import marshmallow as marsh
from peewee import DateTimeField, Model, PostgresqlDatabase, SqliteDatabase, UUIDField

db: PostgresqlDatabase = PostgresqlDatabase(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
)


class BaseModel(Model):
    """All model classes have to inherit from this base class."""

    class Meta:
        """Set Database"""

        database: SqliteDatabase = db

    class Schema(marsh.Schema):
        """The marshmallow schema all model schemas have to inherit from."""

        id = marsh.fields.UUID(dump_only=True)
        created_at = marsh.fields.DateTime(format="iso", dump_only=True)
        updated_at = marsh.fields.DateTime(format="iso", dump_only=True)

        @abc.abstractmethod
        def _make(self, data: dict) -> "BaseModel":
            """Constructs a model object from a dictionary."""
            raise NotImplementedError()

        @marsh.post_load
        def make(self, data: dict, **_) -> "BaseModel":
            """Constructs a model object from a dictionary."""
            return self._make(data)

    id = UUIDField(primary_key=True, default=uuid4)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def save(self, force_insert=True, only=None):
        """Save the data in the model instance
        See https://docs.peewee-orm.com/en/latest/peewee/api.html#Model.save

        :param force_insert: Force INSERT query, defaults to True
        :param only: Only save the given Field instances, defaults to None
        """
        # As `save` is called from `create`, `updated_at` will also be set  when calling `create`.
        self.updated_at = datetime.now()
        super().save(force_insert, only)

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
