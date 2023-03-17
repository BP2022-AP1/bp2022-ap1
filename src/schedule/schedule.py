from abc import ABC, abstractmethod


class Schedule(ABC):
    """An abstract schedule for spawning SUMO vehicles.
    """

    @classmethod
    @abstractmethod
    def from_json(cls, json_object: str) -> "Schedule":
        """Constructs a schedule from a JSON object.

        :param json_object: The JSON object.
        :type json_object: str
        :return: A schedule.
        :rtype: Schedule
        """
        raise NotImplementedError()

    @abstractmethod
    def maybe_spawn(self, tick: int):
        """Determines whether a vehicle should be spawned at the
        current tick and spawns it if so.

        :param tick: The current tick.
        :type tick: int
        """
        raise NotImplementedError()
