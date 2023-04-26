import pytest

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from tests.decorators import recreate_db_setup


class TestRegularScheduleStrategy:
    """Test the regular schedule strategy"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.parametrize("tick", [0, 900])
    def test_not_spawning_before_start_tick(
        self,
        regular_strategy: RegularScheduleStrategy,
        tick: int,
    ):
        assert not regular_strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize("tick", [20000])
    def test_not_spawning_after_end_tick(
        self, regular_strategy: RegularScheduleStrategy, tick: int
    ):
        assert not regular_strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize("tick", [1000])
    def test_spawning_at_start_tick(
        self,
        regular_strategy: RegularScheduleStrategy,
        tick: int,
    ):
        assert regular_strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize("tick", [1100, 1200, 1300])
    def test_spawning_regularly(
        self,
        regular_strategy: RegularScheduleStrategy,
        tick: int,
    ):
        assert regular_strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize("tick", [1105, 1250, 1355])
    def test_not_spawning_in_between(
        self,
        regular_strategy: RegularScheduleStrategy,
        tick: int,
    ):
        assert not regular_strategy.should_spawn(tick=tick)
