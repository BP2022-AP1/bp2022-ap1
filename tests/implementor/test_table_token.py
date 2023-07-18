from uuid import UUID

import peewee
import pytest

from src.implementor.models import Token
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "init_dict",
    [{}],
)
class TestTokenFailingInit:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, init_dict: dict):
        """Test that an object of a class cannot be saved."""
        with pytest.raises(peewee.IntegrityError):
            Token(**init_dict).save(force_insert=True)


class TestTokenSuccessfulInit:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize(
        "init_dict",
        [
            {
                "name": "Owner",
                "permission": "admin",
                "hashedToken": "hash",
            },
        ],
    )
    def test_create(self, init_dict: dict):
        """Test that a object of a class can be created."""
        obj = Token(
            **init_dict,
        )
        obj.save(force_insert=True)
        assert isinstance(obj, Token)
        assert isinstance(obj.id, UUID)
        assert Token.select().where(Token.id == obj.id).first() == obj

    @pytest.mark.parametrize(
        "init_values, expected_dict",
        [
            (
                {
                    "name": "Owner",
                    "permission": "admin",
                    "hashedToken": "hash",
                },
                {
                    "name": "Owner",
                    "permission": "admin",
                },
            ),
        ],
    )
    def test_serialization(self, init_values: dict, expected_dict: dict):
        """Test that an object of a class can be serialized."""
        obj = Token(
            **init_values,
        )
        serialized_obj = obj.to_dict()
        assert isinstance(serialized_obj["id"], str)
        for key in expected_dict.keys():
            assert serialized_obj[key] == expected_dict[key]
        with pytest.raises(KeyError):
            # We don't need the value of serialized_obj["hashedToken"] because it throws an error
            # pylint: disable-next=pointless-statement
            serialized_obj["hashedToken"]
