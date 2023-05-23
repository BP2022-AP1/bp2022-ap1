from itertools import zip_longest

import pytest

from src.implementor.models import SimulationConfiguration
from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.spawner.spawner import (
    Spawner,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)
from tests.decorators import recreate_db_setup


class TestSpawner:
    """Tests for the Spawner"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_creation_from_configuration(
        self,
        spawner: Spawner,
        spawner_configuration: SpawnerConfiguration,
        event_bus: object,
        mock_train_spawner: object,
    ):
        assert spawner.configuration == spawner_configuration
        assert spawner.event_bus == event_bus
        assert spawner.train_spawner == mock_train_spawner

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

    def test_next_tick(
        self,
        spawner: Spawner,
        mock_train_spawner: object,
        strategy_start_tick: int,
        strategy_end_tick: int,
        regular_strategy_frequency: int,
        random_strategy_spawn_ticks: list[int],
    ):
        regular_spawn_ticks = list(
            range(
                strategy_start_tick, strategy_end_tick + 1, regular_strategy_frequency
            )
        )
        spawn_ticks = sorted(regular_spawn_ticks + random_strategy_spawn_ticks)
        for tick in range(strategy_start_tick, strategy_end_tick + 1):
            spawner.next_tick(tick)
        assert all(
            len(schedule._ticks_to_be_spawned) == 0
            for schedule in spawner._schedules.values()
        )
        assert all(
            history_tick == spawn_tick
            for history_tick, spawn_tick in zip_longest(
                sorted(mock_train_spawner.spawn_history),
                sorted(spawn_ticks),
                fillvalue=None,
            )
        )


class TestSpawnerConfiguration:
    """Tests for the SpawnerConfiguration"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_creation(self, spawner_configuration: SpawnerConfiguration):
        assert (
            SpawnerConfiguration.get_by_id(spawner_configuration.id)
            == spawner_configuration
        )

    def test_serialization(self, spawner_configuration: SpawnerConfiguration):
        obj_dict = spawner_configuration.to_dict()
        del obj_dict["created_at"]
        del obj_dict["updated_at"]
        del obj_dict["readable_id"]

        assert obj_dict == {
            "id": str(spawner_configuration.id),
        }


class TestSpawnerConfigurationXSchedule:
    """Tests for the SpawnerConfigurationXSchedule"""

    @recreate_db_setup
    def setup_method(self):
        pass

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


class SpawnerConfigurationXSimulationConfiguration:
    """Tests for the SpawnerConfigurationXSimulationConfiguration"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures("simulation_configuration, spawner_configuration")
    def test_creation(
        self,
        simulation_configuration: SimulationConfiguration,
        spawner_configuration: SpawnerConfiguration,
    ):
        spawner_x_simulation = SpawnerConfigurationXSimulationConfiguration(
            spawner_configuration=spawner_configuration,
            schedule_configuration=simulation_configuration,
        )
        spawner_x_simulation.save()
        assert spawner_x_simulation.spawner_configuration == spawner_configuration
        assert spawner_x_simulation.schedule_configuration == simulation_configuration

    def test_back_references(
        self,
        simulation_configuration: SimulationConfiguration,
        spawner_configuration: SpawnerConfiguration,
    ):
        spawner_x_simulation = SpawnerConfigurationXSimulationConfiguration(
            spawner_configuration=spawner_configuration,
            schedule_configuration=simulation_configuration,
        )
        spawner_x_simulation.save()
        assert len(simulation_configuration.spawner_configuration_references) == 1
        assert (
            simulation_configuration.spawner_configuration_references[0]
            == spawner_x_simulation
        )
        assert len(spawner_configuration.simulation_configuration_references) == 1
        assert (
            spawner_configuration.simulation_configuration_references[0]
            == spawner_x_simulation
        )

    @pytest.mark.usefixtures("simulation_configuration, spawner_configuration")
    def test_serialization(
        self,
        simulation_configuration: SimulationConfiguration,
        spawner_configuration: SpawnerConfiguration,
    ):
        spawner_x_simulation = SpawnerConfigurationXSimulationConfiguration(
            spawner_configuration=spawner_configuration,
            simulation_configuration=simulation_configuration,
        )
        spawner_x_simulation.save()
        obj_dict = spawner_x_simulation.to_dict()
        del obj_dict["created_at"]
        del obj_dict["updated_at"]
        del obj_dict["readable_id"]

        assert obj_dict == {
            "id": str(spawner_x_simulation.id),
            "spawner_configuration": str(spawner_x_simulation.id),
            "schedule_configuration": str(spawner_x_simulation.id),
        }
