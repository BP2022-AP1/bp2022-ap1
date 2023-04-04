from abc import abstractmethod

import marshmallow as marsh
from peewee import ForeignKeyField

from src.base_model import BaseModel
from src.component import Component
from src.schedule.schedule import Schedule


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
        schedule_id = marsh.fields.UUID(required=True)

        def _make(self, data: dict) -> "SpawnerConfigurationXSchedule":
            """Constructs a SpawnerConfigurationXSchedule from a dictionary.

            :param data: The dictionary.
            :return: A SpawnerConfigurationXSchedule.
            """
            return SpawnerConfigurationXSchedule(**data)

    spawner_configuration_id = ForeignKeyField(
        SpawnerConfiguration, null=False, backref="schedules"
    )
    schedule_id = ForeignKeyField(Schedule, null=False)


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
