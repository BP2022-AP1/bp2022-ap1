from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.implementor.models import SimulationConfiguration
from tests.decorators import recreate_db_setup


class TestSimulationConfigurationFailingInit:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize(
        "init_dict",
        [],
    )
    def test_create(self, init_dict: dict):
        """Test that an object of a class cannot be saved."""
        with pytest.raises(peewee.IntegrityError):
            SimulationConfiguration(init_dict).save(force_insert=True)

    @pytest.mark.parametrize(
        "init_dict",
        [],
    )
    def test_deserialization(self, init_dict: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            SimulationConfiguration.Schema().load({**init_dict})


class TestSimulationConfigurationSuccessfulInit:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize(
        "init_dict",
        [
            {
                "description": "description",
            },
            {},
        ],
    )
    def test_create(self, init_dict: dict):
        """Test that a object of a class can be created."""
        obj = SimulationConfiguration(**init_dict)
        obj.save(force_insert=True)
        assert isinstance(obj, SimulationConfiguration)
        assert isinstance(obj.id, UUID)
        assert (
            SimulationConfiguration.select()
            .where(SimulationConfiguration.id == obj.id)
            .first()
            == obj
        )

    # pylint: disable=duplicate-code
    # will change, when adding foreign keys
    @pytest.mark.parametrize(
        "init_values, expected_dict",
        [
            (
                {
                    "description": "description",
                },
                {
                    "description": "description",
                },
            ),
            ({}, {"description": None}),
        ],
    )
    def test_serialization(self, init_values: dict, expected_dict: dict):
        """Test that an object of a class can be serialized."""
        obj = SimulationConfiguration(
            **init_values,
        )

        serialized_obj = obj.to_dict()
        assert isinstance(serialized_obj["id"], str)
        for key in expected_dict.keys():
            assert serialized_obj[key] == expected_dict[key]

    @pytest.mark.parametrize(
        "init_dict, expected_values",
        [
            (
                {
                    "description": "description",
                },
                {
                    "description": "description",
                },
            ),
            ({}, {"description": None}),
        ],
    )
    def test_deserialization(self, init_dict: dict, expected_values: dict):
        """Test that an object of a class can be deserialized."""
        obj = SimulationConfiguration.Schema().load({**init_dict})
        assert isinstance(obj, SimulationConfiguration)
        assert isinstance(obj.id, UUID)
        for key in expected_values.keys():
            assert getattr(obj, key) == expected_values[key]

    # pylint: enable=duplicate-code
    # will change, when adding foreign keys
