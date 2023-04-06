from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy


class RegularScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns vehicles at regular intervals."""

    @classmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Constructs a RegularScheduleStrategy from a ScheduleConfiguration.

        :param schedule_configuration: The ScheduleConfiguration
        :return: A RegularScheduleStrategy
        """
        assert schedule_configuration.strategy_type == "RegularScheduleStrategy"
        return cls(
            start_tick=schedule_configuration.regular_strategy_start_tick,
            frequency=schedule_configuration.regular_strategy_frequency,
        )

    start_tick: int
    frequency: int

    def __init__(self, start_tick: int, frequency: int):
        """Initializer for RegularScheduleStrategy

        :param start_tick: The tick when train spawning should start
        :param frequency: The frquency at which trains should spawn
        """
        self.start_tick = start_tick
        self.frequency = frequency

    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        :return: True if a vehicle should be spawned, False otherwise
        """
        return (
            tick >= self.start_tick and (tick - self.start_tick) % self.frequency == 0
        )
