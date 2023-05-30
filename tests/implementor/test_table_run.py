from uuid import UUID

import peewee
import pytest

from src.implementor.models import Run, SimulationConfiguration, Token
from tests.decorators import recreate_db_setup


class TestRunFailingInit:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize(
        "init_dict",
        [
            {  # simulation_configuration does not exists
                "simulation_configuration": "00000000-0000-0000-0000-000000000000",
            },
            {},  # simulation_configuration is missing
        ],
    )
    def test_create(self, init_dict: dict):
        """Test that an object of a class cannot be saved."""
        with pytest.raises(peewee.IntegrityError):
            Run(**init_dict).save(force_insert=True)


class TestRunSuccessfulInit:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def token(self):
        token = Token(name="owner", permission="admin", hashedToken="hash")
        token.save()
        return token

    @pytest.fixture
    def simulation_configuration(self, token):
        simulation_configuration = SimulationConfiguration(token=token.id)
        simulation_configuration.save()
        return simulation_configuration

    @pytest.mark.parametrize(
        "init_dict",
        [{}, {"process_id": "00000000-0000-0000-0000-000000000000"}],
    )
    def test_create(
        self, init_dict: dict, simulation_configuration: SimulationConfiguration
    ):
        """Test that a object of a class can be created."""
        obj = Run(
            **init_dict,
            simulation_configuration=simulation_configuration.id,
        )
        obj.save(force_insert=True)
        assert isinstance(obj, Run)
        assert isinstance(obj.id, UUID)
        assert isinstance(obj.simulation_configuration, SimulationConfiguration)
        assert obj.simulation_configuration == simulation_configuration
        assert Run.select().where(Run.id == obj.id).first() == obj

    # pylint: disable=duplicate-code
    # will change, when adding foreign keys
    @pytest.mark.parametrize(
        "init_values, expected_dict",
        [
            ({}, {}),
            (
                {"process_id": "00000000-0000-0000-0000-000000000000"},
                {"process_id": "00000000-0000-0000-0000-000000000000"},
            ),
        ],
    )
    def test_serialization(
        self,
        init_values: dict,
        expected_dict: dict,
        simulation_configuration: SimulationConfiguration,
    ):
        """Test that an object of a class can be serialized."""
        obj = Run(
            **init_values,
            simulation_configuration=simulation_configuration.id,
        )
        serialized_obj = obj.to_dict()
        assert isinstance(serialized_obj["id"], str)
        assert isinstance(serialized_obj["simulation"], str)
        assert isinstance(serialized_obj["process_id"], str)
        assert serialized_obj["simulation"] == str(simulation_configuration.id)
        for key in expected_dict.keys():
            assert serialized_obj[key] == expected_dict[key]

    # pylint: enable=duplicate-code
    # will change, when adding foreign keys
