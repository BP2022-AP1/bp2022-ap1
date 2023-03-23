"""
This module contains the fault injector class
"""

from src.component import Component


class FaultInjector(Component):
    """
    Class for fault injection. Faults can be injected into the interlockingController, the Spawner and the Wrapper
    """

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
