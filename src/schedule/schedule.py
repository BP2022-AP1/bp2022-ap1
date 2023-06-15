from abc import ABC, abstractmethod
from typing import Protocol

from src.schedule.demand_schedule_strategy import DemandScheduleStrategy
from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy
from src.wrapper.train_builder import TrainBuilder


class SpawnerProtocol(Protocol):
    """Protocol for the Spawner"""

    train_spawner: TrainBuilder


class Schedule(ABC):
    """An abstract schedule for spawning SUMO vehicles."""

    id: str
    _blocked: bool
    _seconds_to_be_spawned: list[int]
    strategy: ScheduleStrategy

    STRATEGY_CLASSES: dict[str, type] = {
        "RegularScheduleStrategy": RegularScheduleStrategy,
        "RandomScheduleStrategy": RandomScheduleStrategy,
        "DemandScheduleStrategy": DemandScheduleStrategy,
    }

    @classmethod
    def strategy_from_schedule_configuration(
        cls, schedule_configuration: ScheduleConfiguration
    ) -> ScheduleStrategy:
        """Dynamically cosntructs a ScheduleStrategy from a ScheduleConfiguration

        :param schedule_configuration: The Schedule configuration
        :return: A ScheduleStrategy
        """
        strategy_type = schedule_configuration.strategy_type
        strategy_class = cls.STRATEGY_CLASSES[strategy_type]
        assert issubclass(strategy_class, ScheduleStrategy)
        return strategy_class.from_schedule_configuration(schedule_configuration)

    def __init__(self, strategy: ScheduleStrategy, id_: str):
        """Constructs a Schedule."""
        self._blocked = False
        self._seconds_to_be_spawned = []
        self.strategy = strategy
        self.id = id_  # pylint: disable=invalid-name

    @abstractmethod
    def _spawn(self, spawner: SpawnerProtocol, seconds: int) -> bool:
        """Spawns a vehicle.

        :param spawner: The calling Spawner.
        :param seconds: The elapsed seconds
        """
        raise NotImplementedError()

    def maybe_spawn(self, seconds: int, spawner: SpawnerProtocol):
        """Spawns a vehicle if the schedule strategy allows it.

        :param seconds: The elapsed seconds
        :param spawner: The calling spawner.
        """
        if not self._blocked and self.strategy.should_spawn(seconds):
            self._seconds_to_be_spawned.append(seconds)

        if len(self._seconds_to_be_spawned) > 0:
            if self._spawn(spawner, self._seconds_to_be_spawned[-1]):
                self._seconds_to_be_spawned.pop()

    def block(self):
        """Blocks the schedule.

        :raises RuntimeError: when the schedule is already blocked
        """
        if self._blocked:
            raise RuntimeError(f"Schedule {self.id} is already blocked")
        self._blocked = True

    def unblock(self):
        """Unblocks the schedule.

        :raises RuntimeError: when the schedule is already unblocked
        """
        if not self._blocked:
            raise RuntimeError(f"Schedule {self.id} is already unblocked")
        self._blocked = False
