from random import Random

from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy


class RandomScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns trains randomly with a given probability"""

    @classmethod
    def from_schedule_configuration(
        cls, schedule_configuration: ScheduleConfiguration
    ) -> "RandomScheduleStrategy":
        """Constructs a RandomScheduleStrategy from a ScheduleConfiguration

        :param schedule_configuration: The ScheduleConfiguration
        :return: A RandomScheduleStrategy
        """
        assert schedule_configuration.strategy_type == "RandomScheduleStrategy"
        return cls(
            start_time=schedule_configuration.strategy_start_time,
            end_time=schedule_configuration.strategy_end_time,
            trains_per_1000_seconds=schedule_configuration.random_strategy_trains_per_1000_seconds,
            seed=schedule_configuration.random_strategy_seed,
        )

    trains_per_1000_seconds: float
    _random_number_generator: Random

    def __init__(
        self,
        start_time: int,
        end_time: int,
        trains_per_1000_seconds: float,
        seed: int = None,
    ):
        """Constructs a RandomScheduleStrategy

        :param start_time: The time in seconds when train spawning should start
        :param end_tick: The time in seconds when train spawning should end
        :param trains_per_1000_seconds: The probability that a train will spawn in a given amout of time
        :param seed: Seed for the random number generator, defaults to None
        """
        super().__init__(start_time, end_time)
        self.trains_per_1000_seconds = trains_per_1000_seconds
        self._random_number_generator = Random(seed)

    def should_spawn(self, seconds: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param seconds: The elapsed seconds
        :return: True if a vehicle should be spawned, False otherwise
        """
        return (
            super().should_spawn(seconds)
            and self._random_number_generator.random() * 1000
            < self.trains_per_1000_seconds
        )
