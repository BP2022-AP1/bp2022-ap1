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
            start_tick=schedule_configuration.strategy_start_tick,
            end_tick=schedule_configuration.strategy_end_tick,
            trains_per_1000_ticks=schedule_configuration.random_strategy_trains_per_1000_ticks,
            seed=schedule_configuration.random_strategy_seed,
        )

    trains_per_1000_ticks: float
    _random_number_generator: Random

    def __init__(
        self,
        start_tick: int,
        end_tick: int,
        trains_per_1000_ticks: float,
        seed: int = None,
    ):
        """Constructs a RandomScheduleStrategy

        :param start_tick: The tick when train spawning should start
        :param end_tick: The tick when train spawning should end
        :param trains_per_1000_ticks: The probability that a train will spawn in a given tick
        :param seed: Seed for the random number generator, defaults to None
        """
        super().__init__(start_tick, end_tick)
        self.trains_per_1000_ticks = trains_per_1000_ticks
        self._random_number_generator = Random(seed)

    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        :return: True if a vehicle should be spawned, False otherwise
        """
        return (
            super().should_spawn(tick)
            and self._random_number_generator.random() * 1000
            < self.trains_per_1000_ticks
        )
