from src import implementor as impl
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSimulationConfiguration,
)


class TestSpawnerConfiguration:
    def test_get_all_spawner_configuration_ids(self, token, spawner_configuration_data):
        config = SpawnerConfiguration.create(**spawner_configuration_data)

        response = impl.component.get_all_spawner_configuration_ids({}, token)
        (result, status) = response
        assert status == 200
        assert str(config.id) in result

    def test_get_all_spawner_configuration_ids(
        self,
        token,
        spawner_configuration_data,
        empty_simulation_configuration,
    ):
        config = SpawnerConfiguration.create(**spawner_configuration_data)
        another_config = SpawnerConfiguration.create(**spawner_configuration_data)
        SpawnerConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            spawner_configuration=config,
        )

        response = impl.component.get_all_spawner_configuration_ids(
            {"simulationId": str(empty_simulation_configuration.id)}, token
        )
        (result, status) = response

        assert status == 200
        assert str(config.id) in result
        assert str(another_config.id) not in result

    def test_create_spawner_configuration(token, spawner_configuration_data):
        response = impl.component.create_spawner_configuration(
            spawner_configuration_data, token
        )
        (result, status) = response
        assert status == 201
        assert result["id"]
        configs = SpawnerConfiguration.select().where(
            SpawnerConfiguration.id == result["id"]
        )
        assert configs.exists()
        config = configs.get()
        schedules = [
            reference.schedule_configuration_id
            for reference in config.schedule_configuration_references
        ]
        for schedule in schedules:
            assert schedule.id in spawner_configuration_data["schedule"]

    def test_create_spawner_configuration_not_found(
        token,
    ):
        response = impl.component.create_spawner_configuration(
            {"schedule": ["00000000-0000-0000-0000-000000000000"]}, token
        )
        (result, status) = response
        assert status == 404
        assert result == "Schedule not found"
