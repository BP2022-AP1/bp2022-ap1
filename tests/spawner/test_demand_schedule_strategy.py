from src.schedule.demand_schedule_strategy import DemandScheduleStrategy
from tests.decorators import recreate_db_setup


class TestDemandScheduleStrategy:
    """Test the demand schedule strategy"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_spawn_at_right_ticks(
        self,
        demand_strategy: DemandScheduleStrategy,
        demand_strategy_spawn_ticks: list[int],
    ):
        for tick in range(0, demand_strategy.end_time * 2):
            if demand_strategy.should_spawn(tick):
                assert tick in demand_strategy_spawn_ticks
