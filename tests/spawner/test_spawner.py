import pytest

from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.spawner.spawner import Spawner, SpawnerConfiguration
from tests.decorators import recreate_db_setup


class TestSpawner:
    """Tests for the Spawner"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures(
        "spawner", "spawner_configuration", "mock_logger", "mock_traci_wrapper"
    )
    def test_creation_from_configuration(
        self,
        spawner: Spawner,
        spawner_configuration: SpawnerConfiguration,
        mock_logger: object,
        mock_traci_wrapper: object,
    ):
        assert spawner.configuration == spawner_configuration
        assert spawner.logger == mock_logger
        assert spawner.traci_wrapper == mock_traci_wrapper

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
