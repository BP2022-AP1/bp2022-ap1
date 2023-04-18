import pytest

from src.schedule.train_schedule import TrainSchedule
from tests.decorators import recreate_db_setup


class TestTrainSchedule:
    """Tests for TrainSchedule"""

    @recreate_db_setup
    def setup_method(self):
        pass

    # Currently Trains are not instantiable.
    # This test will be implemented when Trains are fixed.
    @pytest.mark.usefixtures("regular_train_schedule", "strategy_start_tick")
    def test_spawning(
        self, regular_train_schedule: TrainSchedule, strategy_start_tick: int
    ):
        pass

    @pytest.mark.usefixtures("regular_train_schedule")
    def test_block_blocked_fails(self, regular_train_schedule: TrainSchedule):
        regular_train_schedule.block()
        with pytest.raises(RuntimeError):
            regular_train_schedule.block()

    @pytest.mark.usefixtures("regular_train_schedule")
    def test_unblock_unblocked_fails(self, regular_train_schedule: TrainSchedule):
        regular_train_schedule.block()
        regular_train_schedule.unblock()
        with pytest.raises(RuntimeError):
            regular_train_schedule.unblock()
