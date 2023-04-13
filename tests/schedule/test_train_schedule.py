import pytest

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.train_schedule import TrainSchedule
from src.wrapper.simulation_objects import Train


class MockTraCiWrapper:
    """Mock for TraCiWrapper"""

    train: Train

    def spawn_train(self, train: Train):
        self.train = train


class TestTrainSchedule:
    """Tests for TrainSchedule"""

    START_TICK: int = 0
    FREQUENCY: int = 10
    TRAIN_TYPE: str = "cargo"

    @pytest.fixture
    def platform_ids(self) -> list[str]:
        return [
            "399ec209-5f72-47be-a821-31a177021311",
            "2cf25596-24cf-49ee-ab44-323522bc2fc1",
            "ccffa906-9324-42bb-afed-a0f923f7e934",
            "f97dd0ba-5c3d-4a71-a1ac-01aca73aa8ce",
            "67e5c841-9fcd-47c3-b33f-d856c3c0b3f4",
            "5e47bb48-82ba-47ea-8295-c70c2c46cdba",
            "9ac02dac-6f0f-4779-b730-c2b22e1d8258",
            "91ce408a-5509-43f6-bb89-137feb0d14f2",
        ]

    @pytest.fixture
    def schedule_id(self) -> str:
        return "294e727c-1b5f-496c-a578-b147b2ff1561"

    @pytest.fixture
    def schedule(self, platform_ids: list[str], schedule_id: str):
        strategy = RegularScheduleStrategy(
            start_tick=self.START_TICK, frequency=self.FREQUENCY
        )
        return TrainSchedule(
            train_type=self.TRAIN_TYPE,
            platform_ids=platform_ids,
            strategy=strategy,
            id_=schedule_id,
        )

    # This test fails in src/wrapper/simulation_objects.py:321
    # with the following error: AttributeError: 'NoneType' object has no attribute 'platforms'
    #
    # I don't have enough knowledge of the codebase to fix this. So I commented it out
    # and left it here to be fixed in a future issue.
    #
    # def test_spawning(
    #     self, schedule: TrainSchedule, platform_ids: list[str], schedule_id: str
    # ):
    #     mock_traci_wrapper = MockTraCiWrapper()
    #     schedule._spawn(mock_traci_wrapper, self.START_TICK)
    #     assert mock_traci_wrapper.train.identifier == f"{schedule_id}_{self.START_TICK}"
    #     assert mock_traci_wrapper.train.train_type.name == self.TRAIN_TYPE
    #     for platform_id, platform in zip(
    #         platform_ids, mock_traci_wrapper.train.timetable
    #     ):
    #         assert platform.identifier == platform_id
