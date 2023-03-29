from typing import Protocol
from src.fault_injector.fault_types.fault import Fault

class IFaultInjector(Protocol):

    def add_fault(self, fault: Fault) -> None:
        ...

    def next_tick(self, tick: int) -> None:
        ...
