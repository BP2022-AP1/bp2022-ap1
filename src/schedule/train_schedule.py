import marshmallow as marsh
from peewee import ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel
from src.schedule.schedule import Schedule


class TrainScheduleXSimulationPlatform(BaseModel):
    """A many-to-many relationship between a train schedule and a simulation platform.
    """
    class Schema(BaseModel.Schema):
        """Schema for TrainScheduleXSimulationPlatform.
        """
        train_schedule_id = marsh.fields.UUID(required=True)
        simulation_platform_id = marsh.fields.UUID(required=True)
        index = marsh.fields.Int(required=True)

        def _make(self, data: dict) -> "TrainScheduleXSimulationPlatform":
            """Constructs a TrainScheduleXSimulationPlatform object from a dictionary.

            :param data: the dictionary
            :return: an instance of the model
            """
            return TrainScheduleXSimulationPlatform(**data)

    train_schedule_id = ForeignKeyField("TrainSchedule", null=False, backref="platforms")
    simulation_platform_id = TextField(null=False)
    index = IntegerField(null=False)


class TrainSchedule(Schedule):
    """A schedule for spawning SUMO trains."""

    class Schema(Schedule.Schema):
        """Schema for TrainSchedule.
        """
        train_type = marsh.fields.Str(required=True)

        def _make(self, data: dict) -> "TrainSchedule":
            """Constructs a TrainSchedule object from a dictionary.

            :param data: the dictionary
            :return: an instance of the model
            """
            return TrainSchedule(**data)

    train_type = TextField(null=False)

    def _spawn(self, traci_wrapper: "ITraCiWrapper"):
        """Spawns a train.

        :param traci_wrapper: The TraCI wrapper to give the train to.
        """
        # Trains are not implemented yet.
        raise NotImplementedError()
