from abc import abstractmethod

from src.base_model import BaseModel


class ScheduleStrategy(BaseModel):
    """An abstract ScheduleStrategy.
    ScheduleStartegies implement the decision logic of
    how a schedule determines whether a vehicle should be spawned
    at a given tick.
    """

    class Schema(BaseModel.Schema):
        """Schema for ScheduleStrategy."""

        pass

    @abstractmethod
    def should_spawn(self, tick: int) -> bool:
        """Determines whether a vehicle should be spawned at the current tick

        :param tick: The current tick
        """
        raise NotImplementedError()
