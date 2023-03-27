"""
This module contains the fault injector class
"""

from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class FaultInjector(Component):
    """
    Class for fault injection. Faults can be injected into the interlockingController, the Spawner and the Wrapper
    """

    _faults: list[Fault] = []

    def add_fault_from_json(self, json_faults: list[str]):
        """Adds faults that should be injected to the fault injector

        :param json_faults: The list of faults as JSON objects
        :type json_faults: list[str]
        """

        raise NotImplementedError()

    def next_tick(self, tick: int):
        """Called by the wrapper to announce the next tick of the simulation

        :param tick: The current simulation tick
        :type tick: int
        """

        raise NotImplementedError()


class IFaultInjector(object):
    """Class that provides an interface to the Faultinjector for other components"""

    def next_tick(self, tick: int):
        raise NotImplementedError()

    def create():
        raise NotImplementedError()
