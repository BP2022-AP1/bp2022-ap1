from src.schedule.schedule import Schedule


class TrainSchedule(Schedule):
    """A schedule for spawning SUMO trains."""

    @classmethod
    def from_json(cls, json_object: str) -> "TrainSchedule":
        """Constructs a TrainSchedule from a JSON object.

        :param json_object: The JSON object.
        :type json_object: str
        :return: A TrainSchedule.
        :rtype: TrainSchedule
        """
        raise NotImplementedError()

    def maybe_spawn(self, tick: int):
        """Determines whether a train should be spawned at the
        current tick and spawns it if so.

        :param tick: The current tick.
        :type tick: int
        """
        raise NotImplementedError()
