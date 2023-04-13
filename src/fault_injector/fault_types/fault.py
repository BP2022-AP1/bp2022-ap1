from abc import ABC, abstractmethod

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.logger.logger import Logger


class Fault(ABC):
    """An abstract fault for the fault injection"""

    configuration: "FaultConfiguration"
    logger: Logger

    def __init__(self, configuration, logger: Logger):
        self.configuration = configuration
        self.logger = logger

    @abstractmethod
    def inject_fault(self, tick: int):
        """injects the fault into the given component"""

        raise NotImplementedError()

    @abstractmethod
    def resolve_fault(self, tick: int):
        """resolves the previously injected fault"""

        raise NotImplementedError()

    def next_tick(self, tick: int):
        """handle the next tick event accordingly

        :param tick: the current simulation tick
        :type tick: int
        """
        if tick == self.configuration.start_tick:
            self.inject_fault(tick=tick)
        elif tick == self.configuration.end_tick:
            self.resolve_fault(tick=tick)
