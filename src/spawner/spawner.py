from abc import ABC, abstractmethod

import marshmallow as marsh
from peewee import ForeignKeyField

from src.base_model import BaseModel
from src.component import Component
from src.logger.logger import Logger
from src.schedule.schedule import Schedule
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.train_schedule import TrainSchedule


class SpawnerConfiguration(BaseModel):
    """Class representing a spawner configuration. It holds a list of
    Schedules which are handled in the reference table class `SpawnerConfigurationXSchedule`.
    This class has no fields except the `id` which is needed by the `Spawner`.
    """

    class Schema(BaseModel.Schema):
        """Marshmallow schema for SpawnerConfiguration"""

        def _make(self, data: dict) -> "SpawnerConfiguration":
            """Constructs a SpawnerConfiguration from a dictionary.

            :param data: The dictionary.
            :return: A SpawnerConfiguration.
            """
            return SpawnerConfiguration(**data)


class SpawnerConfigurationXSchedule(BaseModel):
    """Reference table class for m:n relation
    between SpawnerConfiguration and Schedule.
    """

    class Schema(BaseModel.Schema):
        """Marshmallow schema for SpawnerConfigurationXSchedule"""

        spawner_configuration_id = marsh.fields.UUID(required=True)
        schedule_configuration_id = marsh.fields.UUID(required=True)

        def _make(self, data: dict) -> "SpawnerConfigurationXSchedule":
            """Constructs a SpawnerConfigurationXSchedule from a dictionary.

            :param data: The dictionary.
            :return: A SpawnerConfigurationXSchedule.
            """
            return SpawnerConfigurationXSchedule(**data)

    spawner_configuration_id = ForeignKeyField(
        SpawnerConfiguration, null=False, backref="schedule_configuration_references"
    )
    schedule_configuration_id = ForeignKeyField(ScheduleConfiguration, null=False)


class ISpawnerDisruptor(ABC):
    @abstractmethod
    def block_schedule(self, schedule_id: str):
        """Blocks a schedule.

        :param schedule_id: The id of the schedule to block
        """
        raise NotImplementedError()

    @abstractmethod
    def unblock_schedule(self, schedule_id: str):
        """Unblocks a schedule.

        :param schedule_id: The id of the schedule to unblock
        """
        raise NotImplementedError()


class Spawner(Component, ISpawnerDisruptor):
    """Abstract class for spawners. Spawners can spawn SUMO vehicles
    based on shedules.
    """

    configuration: SpawnerConfiguration
    traci_wrapper: "ITraCiWrapper"
    _schedules: dict[str, Schedule]

    PRIOTITY: int = 0  # This will need to be set to the correct value

    def next_tick(self, tick: int):
        """Called to announce that the next tick occurred.

        :param tick: The current tick.
        :type tick: int
        """
        for schedule in self.schedules:
            schedule.maybe_spawn(tick, self.traci_wrapper)

    def __init__(
        self,
        logger: Logger,
        configuration: SpawnerConfiguration,
        traci_wrapper: "ITraCiWrapper",
    ):
        """Initializes the spawner.

        :param configuration: The configuration.
        :type configuration: SpawnerConfiguration
        """
        # Method resolution order (MRO) is:
        # Spawner -> Component -> ISpawner -> ISpawnerDisruptor -> ABC -> object
        # super(<CLASS>, self).__init__ calls the __init__ method of the next <CLASS> in the MRO
        # call <CLASS>.mro() to see the MRO of <CLASS>
        super(Spawner, self).__init__(logger, self.PRIOTITY)  # calls Component.__init__
        self.configuration = configuration
        self.traci_wrapper = traci_wrapper
        self._load_schedules()

    SCHEDULE_SUBCLASS_MAPPINGS: dict[str, type[Schedule]] = {
        "TrainSchedule": TrainSchedule,
    }

    def _load_schedules(self):
        """Loads the schedules from the database."""
        self._schedules = {}
        for reference in self.configuration.schedule_configuration_references:
            schedule_configuration = reference.schedule_configuration_id
            schedule_subclass = self.SCHEDULE_SUBCLASS_MAPPINGS[
                schedule_configuration.schedule_type
            ]
            schedule = schedule_subclass.from_schedule_configuration(
                schedule_configuration
            )
            self._schedules[schedule.id] = schedule

    def get_schedule(self, schedule_id: str) -> Schedule:
        """Returns the schedule with the given id.

        :param schedule_id: The id of the schedule.
        :return: The schedule.
        """
        return self._schedules[schedule_id]

    def block_schedule(self, schedule_id: str):
        """Blocks a schedule.

        :param schedule_id: The id of the schedule to block
        """
        self._schedules[schedule_id].block()

    def unblock_schedule(self, schedule_id: str):
        """Unblocks a schedule.

        :param schedule_id: The id of the schedule to unblock
        """
        self._schedules[schedule_id].unblock()


# As the spawner perfectly defines its interface we can do the following:
ISpawner = Spawner
