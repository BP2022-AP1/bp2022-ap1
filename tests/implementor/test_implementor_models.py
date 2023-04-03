from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.implementor.models import Run, Token


class TestImplementorModelsToken:
    """Test the Token table and the serialization/deserialization."""

    @pytest.fixture
    def name(self):
        """Name of token owner."""
        return "Hannes"

    @pytest.fixture
    def permission(self):
        """Permission of token."""
        return "admin"

    @pytest.fixture
    def hashed_token(self):
        """Hashed token value."""
        return "hash"

    @pytest.fixture
    def token_as_dict(self, name, permission, hashed_token):
        """A token as dict with all available fields set."""
        return {
            "name": name,
            "permission": permission,
            "hashedToken": hashed_token,
        }

    @pytest.fixture
    def empty_token_as_dict(self):
        """A token as dict without any fields set."""
        return {}

    def test_create(self, token_as_dict):
        """Test that a token can be created."""
        token = Token.create(
            **token_as_dict,
        )
        assert Token.select().where(Token.id == token.id).first() == token

    def test_create_empty_token_fails(self, empty_token_as_dict):
        """Test that a empty Token cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            Token.create(**empty_token_as_dict)

    def test_serialization(self, token_as_dict):
        """Test that a token can be serialized."""
        token = Token.create(
            **token_as_dict,
        )
        assert token.to_dict() == {
            "id": str(token.id),
            **token_as_dict,
        }

    def test_deserialization(self, token_as_dict, name, permission, hashed_token):
        """Test that a token can be deserialized."""
        token = Token.Schema().load(
            token_as_dict,
        )
        assert isinstance(token, Token)
        assert isinstance(token.id, UUID)
        assert token.name == name
        assert token.permission == permission
        assert token.hashedToken == hashed_token

    def test_deserialization_empty_token_fails(self, empty_token_as_dict):
        with pytest.raises(marsh.exceptions.ValidationError):
            Token.Schema().load(empty_token_as_dict)


class TestImplementorModelsRun:
    """Test the run table and the serialization/deserialization"""

    @pytest.fixture
    def run_as_dict(self):
        """Run as dict with all fields set."""
        return {}

    def test_create(self, run_as_dict):
        """Test that a run can be created."""
        run = Run.create(**run_as_dict)
        assert Run.select().where(Run.id == run.id).first() == run

    def test_serialization(self, run_as_dict):
        """Test that a run can be serialized."""
        run = Run.create()
        assert run.to_dict() == {"id": str(run.id), **run_as_dict}

    def test_deserialization(self, run_as_dict):
        """Test that a run can be deserialized."""
        run = Run.Schema().load(run_as_dict)
        assert isinstance(run, Run)
        assert isinstance(run.id, UUID)
