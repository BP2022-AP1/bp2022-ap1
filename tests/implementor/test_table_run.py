from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.implementor.models import Run
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "init_dict",
    [],
)
class TestRunFailingInit:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, init_dict: dict):
        """Test that an object of a class cannot be saved."""
        with pytest.raises(peewee.IntegrityError):
            Run(**init_dict).save(force_insert=True)

    def test_deserialization(self, init_dict: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            Run.Schema().load(init_dict)


class TestRunSuccessfulInit:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize(
        "init_dict",
        [
            {},
        ],
    )
    def test_create(self, init_dict: dict):
        """Test that a object of a class can be created."""
        obj = Run(
            **init_dict,
        )
        obj.save(force_insert=True)
        assert isinstance(obj, Run)
        assert isinstance(obj.id, UUID)
        assert Run.select().where(Run.id == obj.id).first() == obj

    @pytest.mark.parametrize(
        "init_values, expected_dict",
        [
            ({}, {}),
        ],
    )
    def test_serialization(self, init_values: dict, expected_dict: dict):
        """Test that an object of a class can be serialized."""
        obj = Run(
            **init_values,
        )
        serialized_obj = obj.to_dict()
        assert isinstance(serialized_obj["id"], str)
        for key in expected_dict.keys():
            assert serialized_obj[key] == expected_dict[key]

    @pytest.mark.parametrize(
        "init_dict, expected_values",
        [
            ({}, {}),
        ],
    )
    def test_deserialization(self, init_dict: dict, expected_values: dict):
        """Test that an object of a class can be deserialized."""
        obj = Run.Schema().load(
            init_dict,
        )
        assert isinstance(obj, Run)
        assert isinstance(obj.id, UUID)
        for key in expected_values.keys():
            assert getattr(obj, key) == expected_values[key]
