import marshmallow as marsh
from peewee import ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel


class ScheduleConfiguration(BaseModel):
    """Holds information to construct a schedule and its corresponding strategy"""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for ScheduleConfiguration"""

        schedule_type = marsh.fields.String(required=True)
        strategy_type = marsh.fields.String(required=True)

        train_schedule_train_type = marsh.fields.String()

        regular_strategy_start_tick = marsh.fields.Integer()
        regular_strategy_frequency = marsh.fields.Integer()

        def _make(self, data: dict) -> "ScheduleConfiguration":
            """Constructs a ScheduleConfiguration from a dict

            :param data: The dict
            :return: A ScheduleConfiguration
            """
            return ScheduleConfiguration(**data)

    schedule_type = TextField(null=False)
    strategy_type = TextField(null=False)

    train_schedule_train_type = TextField()

    regular_strategy_start_tick = IntegerField()
    regular_strategy_frequency = IntegerField()


class ScheduleConfigurationXSimulationPlatform(BaseModel):
    """Represents the m:n relation betwwen ScheduleConfiguration and SimulationPlatform"""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for ScheduleConfigurationXSimulationPlatform"""

        schedule_configuration_id = marsh.fields.UUID(required=True)
        simulation_platform_id = marsh.fields.UUID(required=True)
        index = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "ScheduleConfigurationXSimulationPlatform":
            """Constructs a ScheduleConfigurationXSimulationPlatform from a dict

            :param data: The dict
            :return: A ScheduleConfigurationXSimulationPlatform
            """
            return ScheduleConfigurationXSimulationPlatform(**data)

    schedule_configuration_id = ForeignKeyField(
        ScheduleConfiguration, null=False, backref="train_schedule_platform_references"
    )
    simulation_platform_id = TextField(null=False)
    index = IntegerField(null=False)
