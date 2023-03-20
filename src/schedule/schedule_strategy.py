from abc import ABC, abstractmethod


class ScheduleStrategy(ABC):
    """An abstract ScheduleStrategy.
    ScheduleStartegies implement the decision logic of
    how a schedule determines whether a vehicle should be spawned
    at a given tick.
    """

    @classmethod
    @abstractmethod
    def from_json(cls, json_object: str) -> "ScheduleStrategy":
        """Constructs a ScheduleStrategy from a JSON object.

        :param json_object: The JSON object.
        :type json_object: str
        :return: A ScheduleStrategy.
        :rtype: ScheduleStrategy
        """
        raise NotImplementedError()

    @abstractmethod
    def maybe_spawn(self, tick: int):
        """Determines whether a train should be spawned at the
        current tick and spawns it if so.

        :param tick: The current tick.
        :type tick: int
        """
        raise NotImplementedError()
