import marshmallow as marsh
from peewee import IntegerField

from src.schedule.schedule_strategy import ScheduleStrategy


class RegularScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns vehicles at regular intervals."""

    class Schema(ScheduleStrategy.Schema):
        """Schema for RegularScheduleStrategy."""

        start_tick = marsh.fields.Int(required=True)
        frequency = marsh.fields.Int(required=True)

        def _make(self, data: dict) -> "RegularScheduleStrategy":
            """Constructs a RegularScheduleStrategy from a dictionary.

            :param data: The dictionary.
            :return: A RegularScheduleStrategy.
            """
            return RegularScheduleStrategy(**data)

    start_tick = IntegerField(null=False)
    frequency = IntegerField(null=False)

    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        :return: True if a vehicle should be spawned, False otherwise
        """
        return (
            tick >= self.start_tick and (tick - self.start_tick) % self.frequency == 0
        )

    def __repr__(self) -> str:
        return f"RegularScheduleStrategy({self.id=}, {self.start_tick=}, {self.frequency=})"
