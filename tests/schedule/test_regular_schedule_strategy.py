from src.schedule.regular_schedule_strategy import RegularScheduleStrategy


def test_not_spawning_before_start_tick():
    strategy = RegularScheduleStrategy(start_tick=1000, frequency=100)
    assert not strategy.should_spawn(tick=900)


def test_spawning_at_start_tick():
    strategy = RegularScheduleStrategy(start_tick=10, frequency=100)
    assert strategy.should_spawn(tick=10)


def test_spawning_regularly():
    strategy = RegularScheduleStrategy(start_tick=10, frequency=100)
    assert strategy.should_spawn(tick=110)
    assert strategy.should_spawn(tick=210)
    assert strategy.should_spawn(tick=310)


def test_not_spawning_in_between():
    strategy = RegularScheduleStrategy(start_tick=10, frequency=100)
    assert not strategy.should_spawn(tick=115)
    assert not strategy.should_spawn(tick=216)
    assert not strategy.should_spawn(tick=317)


def test_de_serialization():
    strategy = RegularScheduleStrategy(start_tick=10, frequency=100)
    serialized = strategy.to_dict()
    deserialized = RegularScheduleStrategy.from_dict(serialized)
    assert strategy.start_tick == deserialized.start_tick
    assert strategy.frequency == deserialized.frequency


def test_database_interaction():
    strategy = RegularScheduleStrategy(start_tick=10, frequency=100)
    strategy.save(force_insert=True)
    id_ = strategy.id
    db_strategy = (
        RegularScheduleStrategy.select()
        .where(RegularScheduleStrategy.id == id_)
        .first()
    )
    assert db_strategy.start_tick == strategy.start_tick
    assert db_strategy.frequency == strategy.frequency
