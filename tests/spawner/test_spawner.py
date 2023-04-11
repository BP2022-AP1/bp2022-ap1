from uuid import uuid4

from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.spawner.spawner import (
    Spawner,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
)
from tests.decorators import recreate_db_setup


class MockTraCiWrapper:
    """Mock for the TraCiWrapper"""


class MockLogger:
    """Mock for the Logger"""


class TestSpawner:
    """Tests for the Spawner"""

    TRAIN_TYPES: list[str] = ["cargo", "passenger"]
    START_TICKS: list[int] = [10, 100]
    FREQUENCIES: list[int] = [100, 42]

    _spawner_configuration: SpawnerConfiguration
    _schedule_configurations: list[ScheduleConfiguration]

    @recreate_db_setup
    def setup_method(self):
        schedule_configuration0 = ScheduleConfiguration(
            schedule_type="TrainSchedule",
            strategy_type="RegularScheduleStrategy",
            train_schedule_train_type=self.TRAIN_TYPES[0],
            regular_strategy_start_tick=self.START_TICKS[0],
            regular_strategy_frequency=self.FREQUENCIES[0],
        )
        schedule_configuration1 = ScheduleConfiguration(
            schedule_type="TrainSchedule",
            strategy_type="RegularScheduleStrategy",
            train_schedule_train_type=self.TRAIN_TYPES[1],
            regular_strategy_start_tick=self.START_TICKS[1],
            regular_strategy_frequency=self.FREQUENCIES[1],
        )
        schedule_configuration0.save()
        schedule_configuration1.save()

        for i in range(8):
            ScheduleConfigurationXSimulationPlatform(
                schedule_configuration_id=schedule_configuration0.id,
                simulation_platform_id=uuid4(),
                index=i,
            ).save()
            ScheduleConfigurationXSimulationPlatform(
                schedule_configuration_id=schedule_configuration1.id,
                simulation_platform_id=uuid4(),
                index=i,
            ).save()

        spawner_configuration = SpawnerConfiguration()
        spawner_configuration.save()

        SpawnerConfigurationXSchedule(
            spawner_configuration_id=spawner_configuration.id,
            schedule_configuration_id=schedule_configuration0.id,
        ).save()
        SpawnerConfigurationXSchedule(
            spawner_configuration_id=spawner_configuration.id,
            schedule_configuration_id=schedule_configuration1.id,
        ).save()

        self._spawner_configuration = spawner_configuration
        self._schedule_configurations = [
            schedule_configuration0,
            schedule_configuration1,
        ]

    def test_creation_from_configuration(self):
        mock_traci_wrapper = MockTraCiWrapper()
        spawner = Spawner(
            logger=MockLogger(),
            configuration=self._spawner_configuration,
            traci_wrapper=MockTraCiWrapper(),
        )
        assert spawner.configuration == self._spawner_configuration
        assert spawner.traci_wrapper == mock_traci_wrapper

    def test_get_schedules(self):
        mock_traci_wrapper = MockTraCiWrapper()
        spawner = Spawner(
            logger=None,
            configuration=self._spawner_configuration,
            traci_wrapper=mock_traci_wrapper,
        )

        schedule_ids = [config.id for config in self._schedule_configurations]
        for i, schedule_id in enumerate(schedule_ids):
            schedule = spawner.get_schedule(schedule_id)
            assert schedule.id == schedule_id
            assert schedule.train_type == self.TRAIN_TYPES[i]
            assert schedule.strategy.start_tick == self.START_TICKS[i]
            assert schedule.strategy.frequency == self.FREQUENCIES[i]
