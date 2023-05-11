import uuid

from src import implementor as impl
from src.implementor.models import SimulationConfiguration


class TestSimulationImplementor:
    def test_get_all_simulation_ids(self, token, empty_simulation_configuration_data):
        simulation = SimulationConfiguration.create(
            **empty_simulation_configuration_data
        )
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
