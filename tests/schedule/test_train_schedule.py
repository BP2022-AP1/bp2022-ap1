from uuid import uuid4
from functools import cache

import pytest

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.train_schedule import TrainSchedule
from src.wrapper.simulation_objects import Train


class MockTraCiWrapper:

    train: Train

    def spawn_train(self, train: Train):
        self.train = train


class TestTrainSchedule:

    PLATFORM_COUNT: int = 8
    START_TICK: int = 0
    FREQUENCY: int = 10
    TRAIN_TYPE: str = "cargo"

    @cache
    @pytest.fixture
    def platform_ids(self) -> list[str]:
        return [uuid4() for _ in range(self.PLATFORM_COUNT)]

    @cache
    @pytest.fixture
    def schedule_id(self) -> str:
        return uuid4()

    @pytest.fixture
    def schedule(self, platform_ids: list[str], schedule_id: str):
        strategy = RegularScheduleStrategy(start_tick=self.START_TICK, frequency=self.FREQUENCY)
        return TrainSchedule(
            train_type=self.TRAIN_TYPE,
            platform_ids=platform_ids,
            strategy=strategy,
            id_=schedule_id
        )

    def test_spawning(self, schedule: TrainSchedule, platform_ids: list[str], schedule_id: str):
        mock_traci_wrapper = MockTraCiWrapper()
        schedule._spawn(mock_traci_wrapper, self.START_TICK)
        assert mock_traci_wrapper.train.identifier == f"{schedule_id}_{self.START_TICK}"
        assert mock_traci_wrapper.train.train_type.name == self.TRAIN_TYPE
        for platform_id, platform in zip(platform_ids, mock_traci_wrapper.train.timetable):
            assert platform.identifier == platform_id
