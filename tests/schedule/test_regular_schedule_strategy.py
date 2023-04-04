import pytest

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy


@pytest.fixture
def regular_strategy() -> RegularScheduleStrategy:
    return RegularScheduleStrategy(start_tick=1000, frequency=100)


@pytest.mark.parametrize(
    "strategy,tick", (("regular_strategy", tick) for tick in [0, 900])
)
def test_not_spawning_before_start_tick(strategy, tick, request):
    strategy = request.getfixturevalue(strategy)
    assert not strategy.should_spawn(tick=tick)


@pytest.mark.parametrize("strategy,tick", [("regular_strategy", 1000)])
def test_spawning_at_start_tick(strategy, tick, request):
    strategy = request.getfixturevalue(strategy)
    assert strategy.should_spawn(tick=tick)


@pytest.mark.parametrize(
    "strategy,tick", (("regular_strategy", tick) for tick in [1100, 1200, 1300])
)
def test_spawning_regularly(strategy, tick, request):
    strategy = request.getfixturevalue(strategy)
    assert strategy.should_spawn(tick=tick)


@pytest.mark.parametrize(
    "strategy,tick", (("regular_strategy", tick) for tick in [1105, 1250, 1355])
)
def test_not_spawning_in_between(strategy, tick, request):
    strategy = request.getfixturevalue(strategy)
    assert not strategy.should_spawn(tick=tick)


def test_de_serialization(regular_strategy):
    serialized = regular_strategy.to_dict()
    deserialized = RegularScheduleStrategy.from_dict(serialized)
    assert regular_strategy.start_tick == deserialized.start_tick
    assert regular_strategy.frequency == deserialized.frequency


def test_database_interaction(regular_strategy):
    regular_strategy.save(force_insert=True)
    id_ = regular_strategy.id
    db_strategy = (
        RegularScheduleStrategy.select()
        .where(RegularScheduleStrategy.id == id_)
        .first()
    )
    assert db_strategy.start_tick == regular_strategy.start_tick
    assert db_strategy.frequency == regular_strategy.frequency
