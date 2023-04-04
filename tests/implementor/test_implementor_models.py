from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.implementor.models import Run, SimulationConfiguration, Token


class TestImplementorModelsSimulationConfiguration:
    """Test the simulation configuration table and the serialization/deserialization"""

    @pytest.fixture
    def description(self):
        """Description of the simulation configuration."""
        return "test"

    @pytest.fixture
    def simulation_configuration_as_dict(self, description):
        """Simulation configuration as dict with all fields set."""
        return {"description": description}

    @pytest.fixture
    def empty_simulation_configuration_as_dict(self):
        """Simulation configuration as dict with only required fields set."""
        return {}

    def test_create(self, simulation_configuration_as_dict):
        """Test that a simulation configuration can be created."""
        sim = SimulationConfiguration.create(**simulation_configuration_as_dict)
        assert (
            SimulationConfiguration.select()
            .where(SimulationConfiguration.id == sim.id)
            .first()
            == sim
        )

    def test_create_without_description(self, empty_simulation_configuration_as_dict):
        """Test that a simulation configuration can be created without a description."""
        sim = SimulationConfiguration.create(**empty_simulation_configuration_as_dict)
        assert (
            SimulationConfiguration.select()
            .where(SimulationConfiguration.id == sim.id)
            .first()
            == sim
        )

    def test_serialization(self, simulation_configuration_as_dict):
        """Test that a simulation configuration can be serialized."""
        sim = SimulationConfiguration.create(**simulation_configuration_as_dict)
        assert sim.to_dict() == {
            "id": str(sim.id),
            **simulation_configuration_as_dict,
        }

    def test_deserialization(self, simulation_configuration_as_dict, description):
        """Test that a simulation configuration can be deserialized."""
        sim = SimulationConfiguration.Schema().load(simulation_configuration_as_dict)
        assert isinstance(sim, SimulationConfiguration)
        assert isinstance(sim.id, UUID)
        assert sim.description == description

    def test_deserialization_without_description(
        self, empty_simulation_configuration_as_dict
    ):
        """Test that a simulation configuration can be deserialized without a description."""
        sim = SimulationConfiguration.Schema().load(
            empty_simulation_configuration_as_dict,
        )
        assert isinstance(sim, SimulationConfiguration)
        assert isinstance(sim.id, UUID)
        assert sim.description is None


class TestImplementorModelsToken:
    """Test the token table and the serialization/deserialization."""

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
