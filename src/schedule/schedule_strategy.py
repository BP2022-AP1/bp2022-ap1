from abc import ABC, abstractmethod

from src.schedule.schedule_configuration import ScheduleConfiguration


class ScheduleStrategy(ABC):
    """An abstract ScheduleStrategy.
    ScheduleStartegies implement the decision logic of
    how a schedule determines whether a vehicle should be spawned
    at a given tick.
    """

    @classmethod
    @abstractmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Constructs a RegularScheduleStrategy from a ScheduleConfiguration.

        :param schedule_configuration: The ScheduleConfiguration
        :return: A ScheduleStrategy
        """
        raise NotImplementedError()

    @abstractmethod
    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        """
        raise NotImplementedError()
