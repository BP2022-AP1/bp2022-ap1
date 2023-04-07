from src.schedule.schedule import Schedule
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy
from src.wrapper.simulation_objects import Train


class TrainSchedule(Schedule):
    """A schedule for spawning SUMO trains."""

    @classmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Constructs a TrainSchedule from a ScheduleConfiguration

        :param schedule_configuration: The ScheduleConfiguration
        :return: A TrainSchedule
        """
        assert schedule_configuration.strategy_type == "TrainSchedule"
        platform_ids = [
            platform_reference.id
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

    def _spawn(self, traci_wrapper: "ITraCiWrapper", tick: int):
        """Spawns a train.

        :param traci_wrapper: The TraCi wrapper to give the train to.
        :param tick: The current tick
        """
        train = Train(f"{self.id}_{tick}", self.platform_ids, self.train_type)
        traci_wrapper.spawn_train(train)
