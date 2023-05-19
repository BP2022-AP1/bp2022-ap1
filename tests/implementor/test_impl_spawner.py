from src import implementor as impl
from src.implementor.models import SimulationConfiguration
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSimulationConfiguration,
)


class TestSpawnerConfiguration:
    def test_get_single_spawner_configuration(self, token, spawner_configuration):
        result, status = impl.component.get_spawner_configuration(
            {"identifier": str(spawner_configuration.id)}, token
        )
        assert status == 200
        schedules = [
            str(reference.schedule_configuration_id.id)
            for reference in spawner_configuration.schedule_configuration_references
        ]
        for schedule_id in result["schedule"]:
            assert schedule_id in schedules

    def test_get_single_spawner_configuration_not_found(self, token):
        result, status = impl.component.get_spawner_configuration(
            {"identifier": "00000000-0000-0000-0000-000000000000"}, token
        )
        assert status == 404
        assert result == "Id not found"

    def test_delete_spawner_configuration(self, token, spawner_configuration):
        result, status = impl.component.delete_spawner_configuration(
            {"identifier": str(spawner_configuration.id)}, token
        )
        assert status == 204
        assert result == "Deleted spawner"
        assert not (
            SpawnerConfiguration.select()
            .where(SpawnerConfiguration.id == str(spawner_configuration.id))
            .exists()
        )

    def test_delete_spawner_configuration_not_found(self, token):
        result, status = impl.component.delete_spawner_configuration(
            {"identifier": "00000000-0000-0000-0000-000000000000"}, token
        )
        assert status == 404
        assert result == "Id not found"

    def test_delete_spawner_configuration_not_allowed(
        self, token, spawner_configuration
    ):
        simulation = SimulationConfiguration()
        simulation.save()
        SpawnerConfigurationXSimulationConfiguration(
            spawner_configuration=spawner_configuration,
            simulation_configuration=simulation,
        ).save()
        result, status = impl.component.delete_spawner_configuration(
            {"identifier": str(spawner_configuration.id)}, token
        )
        assert status == 400
        assert (
            result
            == "Spawner configuration is referenced by a simulation configuration"
        )
