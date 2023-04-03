from uuid import UUID

import pytest

from src.implementor.models import SimulationConfiguration, Run


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
