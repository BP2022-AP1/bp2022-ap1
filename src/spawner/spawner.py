from abc import abstractmethod

from src.component import Component
from src.schedule.schedule import Schedule


class Spawner(Component):
    """Abstract class for spawners. Spawners can spawn SUMO vehicles
    based on shedules.
    """

    @classmethod
    @abstractmethod
    def from_json(cls, json_object: str) -> "Spawner":
        """Constructs a spawner from a JSON object.

        :param json_object: The JSON object.
        :type json_object: str
        :return: A spawner.
        :rtype: Spawner
        """
        raise NotImplementedError()

    @abstractmethod
    def add_schedules_from_json(self, json_schedules: list[str]):
        """Adds schedules to the spawner from a list of JSON objects.

        :param json_schedules: The list of JSON objects.
        :type json_schedules: list[str]
        """
        raise NotImplementedError()

    @abstractmethod
    def spawn_specific(self, schedule: Schedule):
        """Spawns vehicles based on a schedule.

        :param schedule: The schedule.
        :type schedule: Schedule
        """
        raise NotImplementedError()
