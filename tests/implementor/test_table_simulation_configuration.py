from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.implementor.models import SimulationConfiguration, Token
from tests.decorators import recreate_db_setup


class TestSimulationConfigurationFailingInit:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize(
        "init_dict",
        [
            {  # token does not exists
                "token": "00000000-0000-0000-0000-000000000000",
            },
            {},  # token is missing
        ],
    )
    def test_create(self, init_dict: dict):
        """Test that an object of a class cannot be saved."""
        with pytest.raises(peewee.IntegrityError):
            SimulationConfiguration(**init_dict).save(force_insert=True)

    @pytest.mark.parametrize(
        "init_dict",
        [
            {},  # token is missing
        ],
    )
    def test_deserialization(self, init_dict: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            SimulationConfiguration.Schema().load(init_dict)


class TestSimulationConfigurationSuccessfulInit:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def token(self):
        token = Token(name="owner", permission="admin", hashedToken="hash")
        token.save()
        return token

    @pytest.mark.parametrize(
        "init_dict",
        [
            {
                "description": "description",
            },
            {},
        ],
    )
    def test_create(self, init_dict: dict, token: Token):
        """Test that a object of a class can be created."""
        obj = SimulationConfiguration(
            **init_dict,
            token=token.id,
        )
        obj.save(force_insert=True)
        assert isinstance(obj, SimulationConfiguration)
        assert isinstance(obj.id, UUID)
        assert isinstance(obj.token, Token)
        assert obj.token == token
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
    def test_serialization(self, init_values: dict, expected_dict: dict, token: Token):
        """Test that an object of a class can be serialized."""
        obj = SimulationConfiguration(
            **init_values,
            token=token.id,
        )

        serialized_obj = obj.to_dict()
        assert isinstance(serialized_obj["id"], str)
        assert isinstance(serialized_obj["token"], str)
        assert serialized_obj["token"] == str(token.id)
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
    def test_deserialization(
        self, init_dict: dict, expected_values: dict, token: Token
    ):
        """Test that an object of a class can be deserialized."""
        obj = SimulationConfiguration.Schema().load({**init_dict, "token": token.id})
        assert isinstance(obj, SimulationConfiguration)
        assert isinstance(obj.id, UUID)
        assert isinstance(obj.token, Token)
        assert obj.token == token
        for key in expected_values.keys():
            assert getattr(obj, key) == expected_values[key]

    # pylint: enable=duplicate-code
    # will change, when adding foreign keys
