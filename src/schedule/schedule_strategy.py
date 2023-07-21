from abc import ABC, abstractmethod

from src.schedule.schedule_configuration import ScheduleConfiguration


class ScheduleStrategy(ABC):
    """An abstract ScheduleStrategy.
    ScheduleStartegies implement the decision logic of
    how a schedule determines whether a vehicle should be spawned
    at a given time.
    """

    start_time: int
    end_time: int

    def __init__(self, start_time: int, end_time: int):
        """Initializer for ScheduleStrategy

        :param start_time: The time in seconds when train spawning should start
        :param end_time: The time in seconds when train spawning should end
        """
        self.start_time = start_time
        self.end_time = end_time

    @classmethod
    @abstractmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Constructs a RegularScheduleStrategy from a ScheduleConfiguration.

        :param schedule_configuration: The ScheduleConfiguration
        :return: A ScheduleStrategy
        """
        raise NotImplementedError()

    def should_spawn(self, seconds: int) -> bool:
        """Determines whether a vehicle should be spawned at the current time

        :param seconds: The elapsed seconds
        """
        is_after_start_second = seconds >= (self.start_time if self.start_time else 0)
        is_before_end_second = seconds <= (self.end_time if self.end_time else seconds)
        return is_after_start_second and is_before_end_second
