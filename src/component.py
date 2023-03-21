from abc import ABC, abstractmethod
from logger.logger import Logger


class Component(ABC):
    """Interface for components that receive ticks."""

    logger: Logger
    priority: int

    def __init__(self, logger: Logger, priority: int):
        """Initializes the component.

        :param logger: reference to the gobal logger
        :param priority: priority of the component for sorting purposes
        """
        self.logger = logger
        self.priority = priority

    @abstractmethod
    def next_tick(self, tick: int):
        """
        Called to announce that the next tick occurred.
        :param tick: The current tick.
        :rtype: None
        """
        raise NotImplementedError()
