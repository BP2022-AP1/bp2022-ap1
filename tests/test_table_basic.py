from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.base_model import BaseModel
from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "table_class, object_as_dict",
    [
        (
            Token,
            {},
        ),
        (
            PlatformBlockedFaultConfiguration,
            {},
        ),
    ],
)
class TestFailingDict:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, table_class: BaseModel, object_as_dict: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            table_class.create(
                **object_as_dict,
            )

    def test_deserialization(self, table_class: BaseModel, object_as_dict: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            table_class.Schema().load(object_as_dict)


@pytest.mark.parametrize(
    "table_class, object_as_dict",
    [
        (
            Token,
            {
                "name": "Owner",
                "permission": "admin",
                "hashedToken": "hash",
            },
        ),
        (
            PlatformBlockedFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "PlatformBlockedFault",
                "affected_element_id": "12345678",
            },
        ),
        (Run, {}),
        (SimulationConfiguration, {"description": "test"}),
        (SimulationConfiguration, {}),
    ],
)
class TestCorrectFilledDict:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, table_class: BaseModel, object_as_dict: dict):
        """Test that a object of a class can be created."""
        obj = table_class.create(
            **object_as_dict,
        )
        assert table_class.select().where(table_class.id == obj.id).first() == obj

    def test_serialization(self, table_class: BaseModel, object_as_dict: dict):
        """Test that an object of a class can be serialized."""
        obj = table_class.create(
            **object_as_dict,
        )

        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]

        none_fields = (
            set(table_class.Schema().fields.keys())
            - set(object_as_dict.keys())
            - set(["id"])
        )
        for key in none_fields:
            assert getattr(obj, key) is None

    def test_deserialization_full_dict(
        self, table_class: BaseModel, object_as_dict: dict
    ):
        """Test that an object of a class can be deserialized."""
        obj = table_class.Schema().load(
            object_as_dict,
        )
        assert isinstance(obj, table_class)
        assert isinstance(obj.id, UUID)
        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]
