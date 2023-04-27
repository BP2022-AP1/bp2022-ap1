from abc import ABC, abstractmethod
from typing import Protocol

from src.schedule.demand_schedule_strategy import DemandScheduleStrategy
from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy
from src.wrapper.train_spawner import TrainSpawner


class SpawnerProtocol(Protocol):
    """Protocol for the Spawner"""

    train_spawner: TrainSpawner


class Schedule(ABC):
    """An abstract schedule for spawning SUMO vehicles."""

    id: str
    _blocked: bool
    _ticks_to_be_spawned: list[int]
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
        self._ticks_to_be_spawned = []
        self.strategy = strategy
        self.id = id_  # pylint: disable=invalid-name

    @abstractmethod
    def _spawn(self, spawner: SpawnerProtocol, tick: int) -> bool:
        """Spawns a vehicle.

        :param spawner: The calling Spawner.
        :param tick: The current tick
        """
        raise NotImplementedError()

    def maybe_spawn(self, tick: int, spawner: SpawnerProtocol):
        """Spawns a vehicle if the schedule strategy allows it.

        :param tick: The current tick
        :param spawner: The calling spawner.
        """
        if not self._blocked and self.strategy.should_spawn(tick):
            self._ticks_to_be_spawned.append(tick)

        if len(self._ticks_to_be_spawned) > 0:
            if self._spawn(spawner, self._ticks_to_be_spawned[-1]):
                self._ticks_to_be_spawned.pop()

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
