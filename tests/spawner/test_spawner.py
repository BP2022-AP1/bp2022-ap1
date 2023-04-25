import pytest

from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.spawner.spawner import (
    Spawner,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
)
from tests.decorators import recreate_db_setup


class TestSpawner:
    """Tests for the Spawner"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures(
        "spawner", "spawner_configuration", "mock_logger", "mock_train_spawner"
    )
    def test_creation_from_configuration(
        self,
        spawner: Spawner,
        spawner_configuration: SpawnerConfiguration,
        mock_logger: object,
        mock_train_spawner: object,
    ):
        assert spawner.configuration == spawner_configuration
        assert spawner.logger == mock_logger
        assert spawner.train_spawner == mock_train_spawner

    @pytest.mark.usefixtures(
        "spawner",
        "regular_train_schedule_configuration",
        "random_train_schedule_configuration",
    )
    def test_get_schedules(
        self,
        spawner: Spawner,
        regular_train_schedule_configuration: ScheduleConfiguration,
        random_train_schedule_configuration: ScheduleConfiguration,
    ):
        for configuration in [
            regular_train_schedule_configuration,
            random_train_schedule_configuration,
        ]:
            schedule = spawner.get_schedule(configuration.id)
            assert schedule.id == configuration.id
            assert schedule.train_type == configuration.train_schedule_train_type
            assert schedule.strategy.start_tick == configuration.strategy_start_tick
            assert schedule.strategy.end_tick == configuration.strategy_end_tick
            if isinstance(schedule.strategy, RegularScheduleStrategy):
                assert (
                    schedule.strategy.frequency
                    == configuration.regular_strategy_frequency
                )
            elif isinstance(schedule.strategy, RandomScheduleStrategy):
                assert (
                    schedule.strategy.trains_per_1000_ticks
                    == configuration.random_strategy_trains_per_1000_ticks
                )

    @pytest.mark.usefixtures(
        "spawner",
        "mock_train_spawner",
        "strategy_start_tick",
        "strategy_end_tick",
        "regular_strategy_frequency",
        "random_strategy_spawn_ticks"
    )
    def test_next_tick(self, spawner: Spawner, mock_train_spawner: object, strategy_start_tick: int, strategy_end_tick: int, regular_strategy_frequency: int, random_strategy_spawn_ticks: list[int]):
        regular_spawn_ticks = list(
            range(
                strategy_start_tick, strategy_end_tick + 1, regular_strategy_frequency
            )
        )
        spawn_ticks = sorted(regular_spawn_ticks + random_strategy_spawn_ticks)
        for tick in range(strategy_start_tick, strategy_end_tick + 1):
            spawner.next_tick(tick)
        assert set(mock_train_spawner.spawn_history) == set(spawn_ticks)


class TestSpawnerConfiguration:
    """Tests for the SpawnerConfiguration"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures("spawner_configuration")
    def test_creation(self, spawner_configuration: SpawnerConfiguration):
        assert (
            SpawnerConfiguration.get_by_id(spawner_configuration.id)
            == spawner_configuration
        )

    @pytest.mark.usefixtures("spawner_configuration")
    def test_serialization(self, spawner_configuration: SpawnerConfiguration):
        obj_dict = spawner_configuration.to_dict()
        del obj_dict["created_at"]
        del obj_dict["updated_at"]

        assert obj_dict == {
            "id": str(spawner_configuration.id),
        }

    # SpawnerConfiguration currently has no own fields. It only inherits fields
    # from BaseModel. Therefore you can only deserialze an empty dict to
    # crate an instance of SpawnerConfiguration.
    def test_deserialization(self):
        spawner_configuration = SpawnerConfiguration.from_dict({})
        assert spawner_configuration.id is not None


class TestSpawnerConfigurationXSchedule:
    """Tests for the SpawnerConfigurationXSchedule"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures("regular_train_schedule_configuration")
    def test_creation(
        self, regular_train_schedule_configuration: RegularScheduleStrategy
    ):
        spawner_configuration = SpawnerConfiguration()
        spawner_configuration.save()
        spawner_configuration_x_schedule = SpawnerConfigurationXSchedule(
            spawner_configuration_id=spawner_configuration,
            schedule_configuration_id=regular_train_schedule_configuration,
        )
        spawner_configuration_x_schedule.save()
        assert (
            spawner_configuration_x_schedule.spawner_configuration_id
            == spawner_configuration
        )
        assert (
            spawner_configuration_x_schedule.schedule_configuration_id
            == regular_train_schedule_configuration
        )

    @pytest.mark.usefixtures("regular_train_schedule_configuration")
    def test_serialization(
        self, regular_train_schedule_configuration: RegularScheduleStrategy
    ):
        spawner_configuration = SpawnerConfiguration()
        spawner_configuration.save()
        spawner_configuration_x_schedule = SpawnerConfigurationXSchedule(
            spawner_configuration_id=spawner_configuration,
            schedule_configuration_id=regular_train_schedule_configuration,
        )
        spawner_configuration_x_schedule.save()
        obj_dict = spawner_configuration_x_schedule.to_dict()
        del obj_dict["created_at"]
        del obj_dict["updated_at"]

        assert obj_dict == {
            "id": str(spawner_configuration_x_schedule.id),
            "spawner_configuration_id": str(spawner_configuration.id),
            "schedule_configuration_id": str(regular_train_schedule_configuration.id),
        }

    @pytest.mark.usefixtures("regular_train_schedule_configuration")
    def test_deserialization(
        self, regular_train_schedule_configuration: RegularScheduleStrategy
    ):
        spawner_configuration = SpawnerConfiguration()
        spawner_configuration.save()
        spawner_configuration_x_schedule = SpawnerConfigurationXSchedule.from_dict(
            {
                "spawner_configuration_id": str(spawner_configuration.id),
                "schedule_configuration_id": str(
                    regular_train_schedule_configuration.id
                ),
            }
        )
        spawner_configuration_x_schedule.save()
        assert (
            spawner_configuration_x_schedule.spawner_configuration_id
            == spawner_configuration
        )
        assert (
            spawner_configuration_x_schedule.schedule_configuration_id
            == regular_train_schedule_configuration
        )
