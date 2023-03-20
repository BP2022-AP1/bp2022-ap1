from src.schedule.schedule_strategy import ScheduleStrategy


class RegularScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns vehicles at regular intervals."""

    @classmethod
    def from_json(cls, json_object: str) -> "RegularScheduleStrategy":
        """Constructs a RegularScheduleStrategy from a JSON object.

        :param json_object: The JSON object.
        :type json_object: str
        :return: A RegularScheduleStrategy.
        :rtype: RegularScheduleStrategy
        """
        raise NotImplementedError()

    def maybe_spawn(self, tick: int):
        """Determines whether a vehicle should be spawned at the
        current tick and spawns it if so.

        :param tick: The current tick.
        :type tick: int
        """
        raise NotImplementedError()
