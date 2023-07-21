import os

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
        strategy_start_time: int,
    ):
        ticks_per_second = int(1.0 / float(os.environ["TICK_LENGTH"]))
        regular_train_schedule.maybe_spawn(strategy_start_time, spawner)
        assert mock_train_spawner.spawn_history == [strategy_start_time]
        assert (
            int(mock_train_spawner.identifier.split("_")[1]) // ticks_per_second
            == strategy_start_time
        )

    def test_delayed_spawning(
        self,
        spawner: Spawner,
        regular_train_schedule: TrainSchedule,
        mock_train_spawner: object,
        strategy_start_time: int,
        strategy_end_time: int,
        regular_strategy_frequency: int,
    ):
        seconds1, seconds2, seconds3 = list(
            range(
                strategy_start_time, strategy_end_time + 1, regular_strategy_frequency
            )
        )[0:3]
        regular_train_schedule.maybe_spawn(seconds1, spawner)
        assert mock_train_spawner.spawn_history == [seconds1]
        mock_train_spawner.let_next_spawn_fail()
        regular_train_schedule.maybe_spawn(seconds2, spawner)
        assert mock_train_spawner.spawn_history == [seconds1]
        regular_train_schedule.maybe_spawn(seconds3, spawner)
        assert mock_train_spawner.spawn_history == [seconds1, seconds3]
        regular_train_schedule.maybe_spawn(
            seconds3 + regular_strategy_frequency - 1, spawner
        )
        assert mock_train_spawner.spawn_history == [seconds1, seconds3, seconds2]

    def test_block_blocked_fails(self, regular_train_schedule: TrainSchedule):
        regular_train_schedule.block()
        with pytest.raises(RuntimeError):
            regular_train_schedule.block()

    def test_unblock_unblocked_fails(self, regular_train_schedule: TrainSchedule):
        regular_train_schedule.block()
        regular_train_schedule.unblock()
        with pytest.raises(RuntimeError):
            regular_train_schedule.unblock()
