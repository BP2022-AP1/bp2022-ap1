from abc import abstractmethod

import marshmallow as marsh
from peewee import ForeignKeyField

from src.base_model import BaseModel
from src.schedule.schedule_strategy import ScheduleStrategy


class Schedule(BaseModel):
    """An abstract schedule for spawning SUMO vehicles."""

    class Schema(BaseModel.Schema):
        """Schema for Schedule."""

        strategy_id = marsh.fields.UUID(required=True)

    _blocked: bool
    strategy_id: ForeignKeyField(ScheduleStrategy, null=False)

    def __init__(self, *args, **kwargs):
        """Constructs a Schedule."""
        super().__init__(*args, **kwargs)
        self._blocked = False

    @abstractmethod
    def _spawn(self, traci_wrapper: "ITraCiWrapper"):
        """Spawns a vehicle.

        :param traci_wrapper: The TraCI wrapper to give the vehicle to.
        """
        raise NotImplementedError()

    def maybe_spawn(self, tick: int, traci_wrapper: "ITraCiWrapper"):
        """Spawns a vehicle if the schedule strategy allows it.

        :param tick: The current tick
        :param traci_wrapper: The TraCI wrapper to give the spawned vehicle to.
        """
        if not self._blocked and self.strategy.should_spawn(tick):
            self._spawn(traci_wrapper)

    def block(self):
        """Blocks the schedule.

        :raises RuntimeError: when the schedule is already blocked
        """
        if self._blocked:
            raise RuntimeError(f"Schedule {self.id} is already blocked")
        self._blocked = True

    def unblock(self):
        """Unblocks the schedule.

        :raises RuntimeError: when the schedule is already unblocked
        """
        if not self._blocked:
            raise RuntimeError(f"Schedule {self.id} is already unblocked")
        self._blocked = False
