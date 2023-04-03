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
    def maybe_spawn(self, tick: int):
        """Determines whether a train should be spawned at the
        current tick and spawns it if so.

        :param tick: The current tick.
        :type tick: int
        """
        raise NotImplementedError()
