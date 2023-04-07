import pytest

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy


class TestRegularScheduleStrategy:
    """Test the regular schedule strategy"""

    @pytest.fixture
    def regular_strategy(self) -> RegularScheduleStrategy:
        return RegularScheduleStrategy(start_tick=1000, frequency=100)

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

    def test_de_serialization(
        self, regular_strategy: Callable[[None], RegularScheduleStrategy]
    ):
        serialized = regular_strategy.to_dict()
        del serialized["id"]
        del serialized["created_at"]
        del serialized["updated_at"]
        deserialized = RegularScheduleStrategy.from_dict(serialized)
        assert regular_strategy.start_tick == deserialized.start_tick
        assert regular_strategy.frequency == deserialized.frequency

    @recreate_db
    def test_database_interaction(
        self, regular_strategy: Callable[[None], RegularScheduleStrategy]
    ):
        regular_strategy.save(force_insert=True)
        id_ = regular_strategy.id
        db_strategy = (
            RegularScheduleStrategy.select()
            .where(RegularScheduleStrategy.id == id_)
            .first()
        )
        assert db_strategy.start_tick == regular_strategy.start_tick
        assert db_strategy.frequency == regular_strategy.frequency
