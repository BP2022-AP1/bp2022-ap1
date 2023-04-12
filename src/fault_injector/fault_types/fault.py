from abc import ABC, abstractmethod

from src.logger.logger import Logger
from src.component import Component


class Fault(ABC):
    """An abstract fault for the fault injection"""

    configuration: "FaultConfiguration"
    logger: Logger

    def __init__(self, configuration, logger: Logger):
        self.configuration = configuration
        self.logger = logger

    @abstractmethod
    def inject_fault(self):
        """injects the fault into the given component

        :param component: the component the fault should be injected into
        :type component: Component
        """

        raise NotImplementedError()

    @abstractmethod
    def resolve_fault(self):
        """resolves the previously injected fault

        :param component: the component with the injected fault
        :type component: Component
        """

        raise NotImplementedError()

    def next_tick(self, tick: int):
        """handle the next tick event accordingly

        :param tick: the current simulation tick
        :type tick: int
        """
        if tick == self.configuration.start_tick:
            self.inject_fault()
        elif tick == self.configuration.end_tick:
            self.resolve_fault()
