from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from tests.decorators import recreate_db_setup


class TestRandomScheduleStrategy:
    """Test the random schedule strategy"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_spawn_at_right_times(
        self,
        random_strategy: RandomScheduleStrategy,
        random_strategy_spawn_seconds: list[int],
        strategy_end_time: int,
    ):
        for seconds in range(0, strategy_end_time * 2):
            if random_strategy.should_spawn(seconds):
                assert seconds in random_strategy_spawn_seconds
