from typing import Protocol
from src.fault_injector.fault_types.fault import Fault

class IFaultInjector(Protocol):

    def add_fault(self, fault: Fault) -> None:
        """Adds faults that should be injected to the fault injector

        :param json_faults: The list of faults as JSON objects
        :type json_faults: list[str]
        """

    def next_tick(self, tick: int) -> None:
        """Called by the wrapper to announce the next tick of the simulation

        :param tick: The current simulation tick
        :type tick: int
        """
