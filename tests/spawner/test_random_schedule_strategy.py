from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from tests.decorators import recreate_db_setup


class TestRandomScheduleStrategy:
    """Test the random schedule strategy"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_spawn_at_right_ticks(
        self,
        random_strategy: RandomScheduleStrategy,
        random_strategy_spawn_ticks: list[int],
        strategy_end_tick: int,
    ):
        for tick in range(0, strategy_end_tick * 2):
            if random_strategy.should_spawn(tick):
                assert tick in random_strategy_spawn_ticks
