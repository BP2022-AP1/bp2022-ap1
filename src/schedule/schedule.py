from abc import ABC, abstractmethod

from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy


class Schedule(ABC):
    """An abstract schedule for spawning SUMO vehicles."""

    id: str
    _blocked: bool
    strategy: ScheduleStrategy

    STRATEGY_CLASSES: dict[str, type] = {
        "RegularScheduleStrategy": RegularScheduleStrategy,
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
        return strategy_class.from_schedule_configuration(schedule_configruation)

    def __init__(self, strategy: ScheduleStrategy, id_: str):
        """Constructs a Schedule."""
        self._blocked = False
        self.strategy = strategy
        self.id = id_  # pylint: disable=invalid-name

    @abstractmethod
    def _spawn(self, traci_wrapper: "ITraCiWrapper", tick: int):
        """Spawns a vehicle.

        :param traci_wrapper: The TraCi wrapper to give the vehicle to.
        :param tick: The current tick
        """
        raise NotImplementedError()

    def maybe_spawn(self, tick: int, traci_wrapper: "ITraCiWrapper"):
        """Spawns a vehicle if the schedule strategy allows it.

        :param tick: The current tick
        :param traci_wrapper: The TraCi wrapper to give the spawned vehicle to.
        """
        if not self._blocked and self.strategy.should_spawn(tick):
            self._spawn(traci_wrapper, tick)

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
