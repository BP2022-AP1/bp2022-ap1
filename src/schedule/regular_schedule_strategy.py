import marshmallow as marsh
from peewee import IntegerField

from src.schedule.schedule_strategy import ScheduleStrategy


class RegularScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns vehicles at regular intervals."""

    class Schema(ScheduleStrategy.Schema):
        """_summary_

        :param ScheduleStrategy: _description_
        :return: _description_
        """
        start_tick = marsh.fields.Int(required=True)
        frequency = marsh.fields.Int(required=True)

        def _make(self, data: dict) -> "RegularScheduleStrategy":
            """_summary_

            :param data: _description_
            :return: _description_
            """
            return RegularScheduleStrategy(**data)

    start_tick = IntegerField(null=False)
    frequency: IntegerField(null=False)

    def __init__(self, start_tick: int, frequency: int):
        """_summary_

        :param start_tick: _description_
        :param frequency: _description_
        """
        self.start_tick = start_tick
        self.frequency = frequency

    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        """
        return (
            tick >= self.start_tick and (tick - self.start_tick) % self.frequency == 0
        )
