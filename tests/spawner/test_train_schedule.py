import pytest

from src.schedule.train_schedule import TrainSchedule
from src.spawner.spawner import Spawner
from tests.decorators import recreate_db_setup


class TestTrainSchedule:
    """Tests for TrainSchedule"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_spawning(
        self,
        spawner: Spawner,
        regular_train_schedule: TrainSchedule,
        mock_train_spawner: object,
        strategy_start_tick: int,
    ):
        regular_train_schedule.maybe_spawn(strategy_start_tick, spawner)
        assert mock_train_spawner.spawn_history == [strategy_start_tick]
        assert mock_train_spawner.identifier.split("_")[1] == str(strategy_start_tick)

    def test_delayed_spawning(
        self,
        spawner: Spawner,
        regular_train_schedule: TrainSchedule,
        mock_train_spawner: object,
        strategy_start_tick: int,
        strategy_end_tick: int,
        regular_strategy_frequency: int,
    ):
        tick1, tick2, tick3 = list(
            range(
                strategy_start_tick, strategy_end_tick + 1, regular_strategy_frequency
            )
        )[0:3]
        regular_train_schedule.maybe_spawn(tick1, spawner)
        assert mock_train_spawner.spawn_history == [tick1]
        mock_train_spawner.let_next_spawn_fail()
        regular_train_schedule.maybe_spawn(tick2, spawner)
        assert mock_train_spawner.spawn_history == [tick1]
        regular_train_schedule.maybe_spawn(tick3, spawner)
        assert mock_train_spawner.spawn_history == [tick1, tick3]
        regular_train_schedule.maybe_spawn(
            tick3 + regular_strategy_frequency - 1, spawner
        )
        assert mock_train_spawner.spawn_history == [tick1, tick3, tick2]

    def test_block_blocked_fails(self, regular_train_schedule: TrainSchedule):
        regular_train_schedule.block()
        with pytest.raises(RuntimeError):
            regular_train_schedule.block()

    def test_unblock_unblocked_fails(self, regular_train_schedule: TrainSchedule):
        regular_train_schedule.block()
        regular_train_schedule.unblock()
        with pytest.raises(RuntimeError):
            regular_train_schedule.unblock()
