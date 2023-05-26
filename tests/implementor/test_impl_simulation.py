import uuid

import pytest

from src import implementor as impl
from src.implementor.models import Run, SimulationConfiguration, Token
from src.spawner.spawner import SpawnerConfiguration


class TestSimulationImplementor:
    def test_get_all_simulation_ids(self, token):
        simulation = SimulationConfiguration()
        simulation.save()
        result, status = impl.simulation.get_all_simulation_ids(token)
        assert status == 200
        assert str(simulation.id) in result

    def test_post(self, token, simulation_configuration_data: dict):
        result, status = impl.simulation.create_simulation_configuration(
            simulation_configuration_data,
            token,
        )
        assert status == 201
        simulation_configuration_id = result["id"]
        simulation_configuration = (
            SimulationConfiguration.select()
            .where(SimulationConfiguration.id == simulation_configuration_id)
            .get()
        )

        def verify_references(key: str):
            """
            Verifies that the references between the simulation configuration and the component configuration exist
            :param key: The key of the component configuration
            """
            assert set(simulation_configuration_data[key]) == set(
                [
                    getattr(reference, f"{key}_configuration").id
                    for reference in getattr(
                        simulation_configuration, f"{key}_configuration_references"
                    )
                ]
            )

        verify_references("platform_blocked_fault")
        verify_references("schedule_blocked_fault")
        verify_references("track_blocked_fault")
        verify_references("track_speed_limit_fault")
        verify_references("train_prio_fault")
        verify_references("train_speed_fault")

        spawner_ids = [
            reference.spawner_configuration.id
            for reference in simulation_configuration.spawner_configuration_references
        ]
        assert len(spawner_ids) == 1
        assert spawner_ids[0] == simulation_configuration_data["spawner"]

    def test_post_invalid_not_found(self, token):
        simulation_configuration_data = {"spawner": uuid.uuid4()}
        result, status = impl.simulation.create_simulation_configuration(
            simulation_configuration_data,
            token,
        )
        assert status == 404
        assert result["error"] == "Configuration not found"

    def test_get_single_simulation_configuration(
        self, token, simulation_configuration_full
    ):
        run = Run.create(simulation_configuration=simulation_configuration_full)
        result, status = impl.simulation.get_simulation_configuration(
            {"identifier": str(simulation_configuration_full.id)}, token
        )
        assert status == 200

        def verify_references(key: str):
            set(result[key]) == set(
                [
                    str(getattr(reference, f"{key}_configuration").id)
                    for reference in getattr(
                        simulation_configuration_full, f"{key}_configuration_references"
                    )
                ]
            )

        verify_references("platform_blocked_fault")
        verify_references("schedule_blocked_fault")
        verify_references("track_blocked_fault")
        verify_references("track_speed_limit_fault")
        verify_references("train_prio_fault")
        verify_references("train_speed_fault")

        spawners = [
            reference.spawner_configuration
            for reference in simulation_configuration_full.spawner_configuration_references
        ]
        spawner = spawners[0]
        assert result["spawner"] == str(spawner.id)

        assert result["runs"] == [str(run.id)]

    def test_update_simulation_configuration_not_found(self, token):
        result, status = impl.simulation.get_simulation_configuration(
            {"identifier": "00000000-0000-0000-0000-000000000000"}, token
        )
        assert status == 404
        assert result == "Simulation not found"

    def test_update_simulation_configuration_with_run(
        self, token, empty_simulation_configuration
    ):
        Run.create(simulation_configuration=empty_simulation_configuration)
        result, status = impl.simulation.update_simulation_configuration(
            {"identifier": str(empty_simulation_configuration.id)},
            token,
            {},
        )
        assert status == 400
        assert result == "Simulation configuration is used in a run"

    def test_delete_simulation_configuration(
        self, token, simulation_configuration_full
    ):
        result, status = impl.simulation.delete_simulation_configuration(
            {"identifier": str(simulation_configuration_full.id)}, token
        )
        assert status == 204
        assert result == "Deleted simulation"
        assert not (
            SimulationConfiguration.select()
            .where(SimulationConfiguration.id == str(simulation_configuration_full.id))
            .exists()
        )

    def test_delete_simulation_configuration_not_found(self, token):
        result, status = impl.simulation.delete_simulation_configuration(
            {"identifier": "00000000-0000-0000-0000-000000000000"}, token
        )
        assert status == 404
        assert result == "Simulation not found"

    def test_delete_simulation_configuration_with_run(
        self, token, empty_simulation_configuration
    ):
        Run.create(simulation_configuration=empty_simulation_configuration)
        result, status = impl.simulation.delete_simulation_configuration(
            {"identifier": str(empty_simulation_configuration.id)}, token
        )
        assert status == 400
        assert result == "Simulation configuration is used in a run"

    @pytest.mark.parametrize(
        "body_key, body_value_fixture",
        [
            ("platform_blocked_fault", "another_platform_blocked_fault_configuration"),
            ("schedule_blocked_fault", "another_schedule_blocked_fault_configuration"),
            ("track_blocked_fault", "another_track_blocked_fault_configuration"),
            (
                "track_speed_limit_fault",
                "another_track_speed_limit_fault_configuration",
            ),
            ("train_prio_fault", "another_train_prio_fault_configuration"),
            ("train_speed_fault", "another_train_speed_fault_configuration"),
        ],
    )
    def test_update_simulation_configuration_faults(
        self,
        token: Token,
        simulation_configuration_full: SimulationConfiguration,
        body_key: str,
        body_value_fixture: str,
        request: pytest.FixtureRequest,
    ):
        body_value = request.getfixturevalue(body_value_fixture)
        result, status = impl.simulation.update_simulation_configuration(
            {"identifier": str(simulation_configuration_full.id)},
            {
                body_key: [body_value],
            },
            token,
        )
        assert status == 200
        assert result == "Updated simulation configuration"
        new_simulation_configuration = SimulationConfiguration.get_by_id(
            simulation_configuration_full.id
        )
        config_ids = [
            str(getattr(reference, f"{body_key}_configuration").id)
            for reference in getattr(
                new_simulation_configuration, f"{body_key}_configuration_references"
            )
        ]
        assert set(config_ids) == set([str(body_value)])

    def test_update_simulation_configuration_spawner(
        self,
        token: Token,
        simulation_configuration_full: SimulationConfiguration,
        another_spawner_configuration: SpawnerConfiguration,
    ):
        result, status = impl.simulation.update_simulation_configuration(
            {"identifier": str(simulation_configuration_full.id)},
            {
                "spawner": another_spawner_configuration,
            },
            token,
        )
        assert status == 200
        assert result == "Updated simulation configuration"
        new_simulation_configuration = SimulationConfiguration.get_by_id(
            simulation_configuration_full.id
        )
        config_ids = [
            str(reference.spawner_configuration.id)
            for reference in new_simulation_configuration.spawner_configuration_references
        ]
        assert set(config_ids) == set([str(another_spawner_configuration.id)])

    def test_update_simulation_configuration_description(
        self,
        token: Token,
        simulation_configuration_full: SimulationConfiguration,
    ):
        new_description = "new-description"
        result, status = impl.simulation.update_simulation_configuration(
            {"identifier": str(simulation_configuration_full.id)},
            {
                "description": new_description,
            },
            token,
        )
        assert status == 200
        assert result == "Updated simulation configuration"
        new_simulation_configuration = SimulationConfiguration.get_by_id(
            simulation_configuration_full.id
        )
        assert new_simulation_configuration.description == new_description
