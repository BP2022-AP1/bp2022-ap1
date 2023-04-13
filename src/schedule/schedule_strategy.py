from abc import ABC, abstractmethod

from src.schedule.schedule_configuration import ScheduleConfiguration


class ScheduleStrategy(ABC):
    """An abstract ScheduleStrategy.
    ScheduleStartegies implement the decision logic of
    how a schedule determines whether a vehicle should be spawned
    at a given tick.
    """

    start_tick: int
    end_tick: int

    def __init__(self, start_tick: int, end_tick: int):
        """Initializer for ScheduleStrategy

        :param start_tick: The tick when train spawning should start
        """
        self.start_tick = start_tick
        self.end_tick = end_tick

    @classmethod
    @abstractmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Constructs a RegularScheduleStrategy from a ScheduleConfiguration.

        :param schedule_configuration: The ScheduleConfiguration
        :return: A ScheduleStrategy
        """
        raise NotImplementedError()

    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        """
        return tick >= self.start_tick and tick <= (
            self.end_tick if self.end_tick else tick
        )
