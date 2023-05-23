from peewee import DateTimeField, FloatField, ForeignKeyField, IntegerField, TextField

from src.base_model import BaseModel, SerializableBaseModel


class ScheduleConfiguration(SerializableBaseModel):
    """Holds information to construct a schedule and its corresponding strategy"""

    schedule_type = TextField()
    strategy_type = TextField()

    strategy_start_tick = IntegerField(null=True)
    strategy_end_tick = IntegerField(null=True)

    train_schedule_train_type = TextField(null=True)

    regular_strategy_frequency = IntegerField(null=True)

    random_strategy_trains_per_1000_ticks = FloatField(null=True)
    random_strategy_seed = IntegerField(null=True)

    demand_strategy_power_station = TextField(null=True)
    demand_strategy_scaling_factor = FloatField(null=True)
    demand_strategy_start_datetime = DateTimeField(null=True)

    def to_dict(self):
        data = super().to_dict()
        platform_ids = [
            platform.simulation_platform_id
            for platform in ScheduleConfigurationXSimulationPlatform.select()
            .where(
                ScheduleConfigurationXSimulationPlatform.schedule_configuration_id
                == self.id
            )
            .order_by(ScheduleConfigurationXSimulationPlatform.index)
        ]
        return {
            "schedule_type": self.schedule_type,
            "strategy_type": self.strategy_type,
            "strategy_start_tick": self.strategy_start_tick,
            "strategy_end_tick": self.strategy_end_tick,
            "train_schedule_train_type": self.train_schedule_train_type,
            "regular_strategy_frequency": self.regular_strategy_frequency,
            "random_strategy_trains_per_1000_ticks": self.random_strategy_trains_per_1000_ticks,
            "random_strategy_seed": self.random_strategy_seed,
            "demand_strategy_power_station": self.demand_strategy_power_station,
            "demand_strategy_scaling_factor": self.demand_strategy_scaling_factor,
            "demand_strategy_start_datetime": self.demand_strategy_start_datetime,
            "platforms": platform_ids,
            **data,
        }


class ScheduleConfigurationXSimulationPlatform(BaseModel):
    """Represents the m:n relation betwwen ScheduleConfiguration and SimulationPlatform"""

    schedule_configuration_id = ForeignKeyField(
        ScheduleConfiguration, null=False, backref="train_schedule_platform_references"
    )
    simulation_platform_id = TextField(null=False)
    index = IntegerField(null=False)
