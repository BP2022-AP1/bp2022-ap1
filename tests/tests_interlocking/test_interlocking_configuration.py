from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.base_model import BaseModel
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
)
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "object_as_dict",
    [
        {
            "dynamicRouting": True,
        },
    ],
)
class TestCorrectFilledDict:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, object_as_dict: dict):
        """Test that a object of a class can be created."""
        obj = InterlockingConfiguration.create(
            **object_as_dict,
        )
        assert (
            InterlockingConfiguration.select()
            .where(InterlockingConfiguration.id == obj.id)
            .first()
            == obj
        )

    def test_serialization(self, object_as_dict: dict):
        """Test that an object of a class can be serialized."""
        obj = InterlockingConfiguration.create(
            **object_as_dict,
        )

        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]

    def test_deserialization_full_dict(self, object_as_dict: dict):
        """Test that an object of a class can be deserialized."""
        obj = InterlockingConfiguration.Schema().load(
            object_as_dict,
        )
        assert isinstance(obj, InterlockingConfiguration)
        assert isinstance(obj.id, UUID)
        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]
