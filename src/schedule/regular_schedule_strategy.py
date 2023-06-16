from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy


class RegularScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns vehicles at regular intervals."""

    @classmethod
    def from_schedule_configuration(
        cls, schedule_configuration: ScheduleConfiguration
    ) -> "RegularScheduleStrategy":
        """Constructs a RegularScheduleStrategy from a ScheduleConfiguration.

        :param schedule_configuration: The ScheduleConfiguration
        :return: A RegularScheduleStrategy
        """
        assert schedule_configuration.strategy_type == "RegularScheduleStrategy"
        return cls(
            start_time=schedule_configuration.strategy_start_time,
            end_time=schedule_configuration.strategy_end_time,
            frequency=schedule_configuration.regular_strategy_frequency,
        )

    frequency: int

    def __init__(self, start_time: int, end_time: int, frequency: int):
        """Initializer for RegularScheduleStrategy

        :param start_time: The time in seconds when train spawning should start
        :param end_time: The time in seconds when train spawning should end
        :param frequency: The frequency at which trains should spawn
        """
        super().__init__(start_time, end_time)
        self.frequency = frequency

    def should_spawn(self, seconds: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param seconds: The elapsed seconds
        :return: True if a vehicle should be spawned, False otherwise
        """
        return (
            super().should_spawn(seconds)
            and (seconds - self.start_time) % self.frequency == 0
        )
