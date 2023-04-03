from abc import abstractmethod

import marshmallow as marsh
from peewee import ForeignKeyField

from src.base_model import BaseModel
from src.schedule.schedule_strategy import ScheduleStrategy


class Schedule(BaseModel):
    """An abstract schedule for spawning SUMO vehicles."""

    class Schema(BaseModel.Schema):
        strategy = marsh.fields.Nested(ScheduleStrategy.Schema())

    _blocked: bool
    strategy: ForeignKeyField(ScheduleStrategy, primary_key=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._blocked = False

    @abstractmethod
    def _spawn(self, traci_wrapper: "ITraCiWrapper"):
        raise NotImplementedError()

    def maybe_spawn(self, tick: int, traci_wrapper: "ITraCiWrapper"):
        if not self._blocked and self.strategy.should_spawn(tick):
            self._spawn(traci_wrapper)

    def block(self):
        if self._blocked:
            raise RuntimeError(f"Schedule {self.id} is already blocked")
        self._blocked = True

    def unblock(self):
        if not self._blocked:
            raise RuntimeError(f"Schedule {self.id} is already unblocked")
        self._blocked = False
