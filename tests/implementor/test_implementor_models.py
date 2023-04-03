from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.implementor.models import Run, SimulationConfiguration, Token


@pytest.mark.parametrize(
    "Class, object_as_dict",
    [
        (
            Token,
            {},
        ),
    ],
)
class TestFailingDict:
    def test_create(self, Class, object_as_dict):
        """Test that a token cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            Class.create(
                **object_as_dict,
            )

    def test_deserialization(self, Class, object_as_dict):
        """Test that a token can be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            Class.Schema().load(object_as_dict)


@pytest.mark.parametrize(
    "Class, object_as_dict",
    [
        (
            Token,
            {
                "name": "Owner",
                "permission": "admin",
                "hashedToken": "hash",
            },
        ),
        (Run, {}),
        (SimulationConfiguration, {"description": "test"}),
        (SimulationConfiguration, {}),
    ],
)
class TestCorrectFilledDict:
    def test_create(self, Class, object_as_dict):
        """Test that a token can be created."""
        obj = Class.create(
            **object_as_dict,
        )
        assert Class.select().where(Class.id == obj.id).first() == obj

    def test_serialization(self, Class, object_as_dict):
        """Test that a token can be serialized."""
        obj = Class.create(
            **object_as_dict,
        )

        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]

        none_fields = (
            set(Class.Schema().fields.keys()) - set(object_as_dict.keys()) - set(["id"])
        )
        for key in none_fields:
            assert getattr(obj, key) is None

    def test_deserialization_full_dict(self, Class, object_as_dict):
        """Test that a token can be deserialized."""
        obj = Class.Schema().load(
            object_as_dict,
        )
        assert isinstance(obj, Class)
        assert isinstance(obj.id, UUID)
        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]
