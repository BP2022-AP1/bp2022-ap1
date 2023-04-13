import pytest

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy


class TestRegularScheduleStrategy:
    """Test the regular schedule strategy"""

    @pytest.fixture
    def regular_strategy(self) -> RegularScheduleStrategy:
        return RegularScheduleStrategy(start_tick=1000, end_tick=None, frequency=100)

    @pytest.mark.parametrize(
        "strategy,tick", (("regular_strategy", tick) for tick in [0, 900])
    )
    def test_not_spawning_before_start_tick(
        self,
        strategy: RegularScheduleStrategy,
        tick: int,
        request: pytest.FixtureRequest,
    ):
        strategy = request.getfixturevalue(strategy)
        assert not strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize("strategy,tick", [("regular_strategy", 1000)])
    def test_spawning_at_start_tick(
        self,
        strategy: RegularScheduleStrategy,
        tick: int,
        request: pytest.FixtureRequest,
    ):
        strategy = request.getfixturevalue(strategy)
        assert strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize(
        "strategy,tick", (("regular_strategy", tick) for tick in [1100, 1200, 1300])
    )
    def test_spawning_regularly(
        self,
        strategy: RegularScheduleStrategy,
        tick: int,
        request: pytest.FixtureRequest,
    ):
        strategy = request.getfixturevalue(strategy)
        assert strategy.should_spawn(tick=tick)

    @pytest.mark.parametrize(
        "strategy,tick", (("regular_strategy", tick) for tick in [1105, 1250, 1355])
    )
    def test_not_spawning_in_between(
        self,
        strategy: RegularScheduleStrategy,
        tick: int,
        request: pytest.FixtureRequest,
    ):
        strategy = request.getfixturevalue(strategy)
        assert not strategy.should_spawn(tick=tick)
