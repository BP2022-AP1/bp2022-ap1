import os
from datetime import datetime
from uuid import uuid4

import human_readable_ids
from peewee import (
    CharField,
    DateTimeField,
    Model,
    PostgresqlDatabase,
    SqliteDatabase,
    UUIDField,
)

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

    id = UUIDField(primary_key=True, default=uuid4)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    readable_id = CharField()

    def save(self, force_insert=True, only=None):
        """Save the data in the model instance
        See https://docs.peewee-orm.com/en/latest/peewee/api.html#Model.save

        :param force_insert: Force INSERT query, defaults to True
        :param only: Only save the given Field instances, defaults to None
        """
        # As `save` is called from `create`, `updated_at` will also be set  when calling `create`.
        if self.readable_id is None:
            self.readable_id = human_readable_ids.get_new_id()
        self.updated_at = datetime.now()
        super().save(force_insert, only)


class SerializableBaseModel(BaseModel):
    """All model classes have to inherit from this base class
    if they want to have additional serialization features."""

    def to_dict(self) -> dict[str, any]:
        """serializes the model object to a dictionary.

        :return: the dictionary
        """
        return {
            "id": str(self.id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "readable_id": self.readable_id,
        }
