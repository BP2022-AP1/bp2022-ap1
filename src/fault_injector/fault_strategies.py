import os
from abc import ABC, abstractmethod
from random import Random

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)


def tick_to_second(tick: int) -> int:
    """converts a tick into a second"""
    return int(float(tick) * float(os.getenv("TICK_LENGTH")))


class FaultStrategy(ABC):
    """Abstract Strategy class. Classes that inherit from this define the
    injection as well as the resolve behavior of the faults"""

    @abstractmethod
    def should_inject(
        self, tick: int, configuration: FaultConfiguration, injected: bool
    ) -> bool:
        """returns wether or not the fault should be injected at the specific simulation tick

        :param tick: the current simulation tick
        :type tick: int
        :param configuration: the configuration of the Fault
        :type configuration: FaultConfiguration
        :param injected: wether or not the requesting fault is injected at the moment
        :type injected: bool
        :rtype: bool
        """
        raise NotImplementedError()

    @abstractmethod
    def should_resolve(
        self, tick: int, configuration: FaultConfiguration, injected: bool
    ) -> bool:
        """returns wether or not the fault should be resolved at the specific simulation tick

        :param tick: the current simulation tick
        :type tick: int
        :param configuration: the configuration of the Fault
        :type configuration: FaultConfiguration
        :param injected: wether or not the requesting fault is injected at the moment
        :type injected: bool
        :rtype: bool
        """
        raise NotImplementedError()


class RegularFaultStrategy(FaultStrategy):
    """Faults that use this class as their strategy get injected and resolved
    at specific simulation ticks"""

    def should_inject(
        self, tick: int, configuration: FaultConfiguration, injected: bool
    ) -> bool:
        return configuration.start_time == tick_to_second(tick) and not injected

    def should_resolve(
        self, tick: int, configuration: FaultConfiguration, injected: bool
    ) -> bool:
        return configuration.end_time == tick_to_second(tick) and injected


class RandomFaultStrategy(FaultStrategy):
    """Faults that use this class as their strategy get injected and resolved at
    random simulation ticks, controlled by probabilities"""

    random_number_generator: Random = Random()

    def __init__(self, seed: int = None) -> None:
        if seed is not None:
            self.random_number_generator = Random(seed)

    def should_inject(
        self, tick: int, configuration: FaultConfiguration, injected: bool
    ) -> bool:
        return (
            self.random_number_generator.random() < configuration.inject_probability
            and not injected
        )

    def should_resolve(
        self, tick: int, configuration: FaultConfiguration, injected: bool
    ) -> bool:
        return (
            self.random_number_generator.random() < configuration.resolve_probability
            and injected
        )
