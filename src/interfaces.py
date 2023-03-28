from typing import Protocol
from src.fault_injector.fault_types.fault import Fault

class FaultInjector(Protocol):

    def add_fault(fault: Fault) -> None: ...

    def next_tick(tick: int) -> None: ...