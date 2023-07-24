import os

from src.schedule.schedule import Schedule, SpawnerProtocol
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy


class TrainSchedule(Schedule):
    """A schedule for spawning SUMO trains."""

    TICKS_PER_SECOND = int(1.0 / float(os.environ["TICK_LENGTH"]))

    @classmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Constructs a TrainSchedule from a ScheduleConfiguration

        :param schedule_configuration: The ScheduleConfiguration
        :return: A TrainSchedule
        """
        assert schedule_configuration.schedule_type == "TrainSchedule"
        platform_ids = [
            platform_reference.simulation_platform_id
            for platform_reference in sorted(
                schedule_configuration.train_schedule_platform_references,
                key=lambda ref: ref.index,
            )
        ]
        return cls(
            train_type=schedule_configuration.train_schedule_train_type,
            platform_ids=platform_ids,
            strategy=cls.strategy_from_schedule_configuration(schedule_configuration),
            id_=schedule_configuration.id,
        )

    train_type: str
    platform_ids: list[str]

    def __init__(
        self,
        train_type: str,
        platform_ids: list[str],
        strategy: ScheduleStrategy,
        id_: str,
    ):
        """Initializer for TrainSchedule

        :param train_type: The type of the train
        :param platform_ids: A list of platforms the train has to visit
        """
        self.train_type = train_type
        self.platform_ids = platform_ids
        super().__init__(strategy, id_)

    def _spawn(self, spawner: SpawnerProtocol, seconds: int) -> bool:
        """Spawns a vehicle.

        :param spawner: The calling Spawner.
        :param seconds: The elapsed seconds
        :return: if the spawning was successful
        """
        return spawner.train_spawner.spawn_train(
            f"{self.id}_{seconds * self.TICKS_PER_SECOND}_{self.train_type}",
            self.platform_ids,
            self.train_type,
        )
