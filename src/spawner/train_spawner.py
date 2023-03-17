from src.schedule.train_schedule import TrainSchedule
from src.spawner.spawner import Spawner


class TrainSpawner(Spawner):
    """A Spawner able to spawn SUMO trains based on schedules.
    """

    @classmethod
    def from_json(cls, json_object: str) -> "TrainSpawner":
        """Constructs a TrainSpawner from a JSON object.

        :param json_object: The JSON object.
        :type json_object: str
        :return: A TrainSpawner.
        :rtype: TrainSpawner
        """
        raise NotImplementedError()  # TODO: implement this

    def add_schedules_from_json(self, json_schedules: list[str]):
        """Adds train schedules to the TrainSpawner
        from a list of JSON objects.

        :param json_schedules: The list of JSON objects.
        :type json_schedules: list[str]
        """
        raise NotImplementedError()  # TODO: implement this

    def spawn_specific(self, schedule: TrainSchedule):
        """Spawns vehicles based on a train schedule.

        :param schedule: The train schedule.
        :type schedule: TrainSchedule
        """
        raise NotImplementedError()  # TODO: implement this

    def next_tick(self, tick: int):
        """Called to announce that the next tick occurred.

        :param tick: The current tick.
        :type tick: int
        """
        raise NotImplementedError()  # TODO: implement this
