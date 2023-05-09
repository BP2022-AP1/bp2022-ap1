import pytest

from src.implementor.models import SimulationConfiguration
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
    InterlockingConfigurationXSimulationConfiguration,
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
        obj_dict = InterlockingConfiguration.create(**object_as_dict).to_dict()

        for key in object_as_dict.keys():
            assert obj_dict[key] == object_as_dict[key]


class TestInterlockingConfigurationXSimulationConfiguration:
    """Tests for the InterlockingConfigurationXSimulationConfiguration"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def simulation_configuration(self) -> SimulationConfiguration:
        return SimulationConfiguration.create()

    @pytest.mark.usefixtures("simulation_configuration, interlocking_configuration")
    def test_creation(
        self,
        simulation_configuration: SimulationConfiguration,
        interlocking_configuration: InterlockingConfiguration,
    ):
        interlocking_x_simulation = InterlockingConfigurationXSimulationConfiguration(
            interlocking_configuration=interlocking_configuration,
            schedule_configuration=simulation_configuration,
        )
        interlocking_x_simulation.save()
        assert (
            interlocking_x_simulation.interlocking_configuration
            == interlocking_configuration
        )
        assert (
            interlocking_x_simulation.simulation_configuration == simulation_configuration
        )

    def test_back_references(
        self,
        simulation_configuration: SimulationConfiguration,
        interlocking_configuration: InterlockingConfiguration,
    ):
        interlocking_x_simulation = InterlockingConfigurationXSimulationConfiguration(
            interlocking_configuration=interlocking_configuration,
            schedule_configuration=simulation_configuration,
        )
        interlocking_x_simulation.save()
        assert len(simulation_configuration.interlocking_configuration_references) == 1
        assert (
            simulation_configuration.interlocking_configuration_references[0]
            == interlocking_x_simulation
        )
        assert len(interlocking_configuration.simulation_configuration_references) == 1
        assert (
            interlocking_configuration.simulation_configuration_references[0]
            == interlocking_x_simulation
        )
