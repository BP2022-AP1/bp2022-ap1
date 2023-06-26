"""
This module contains the fault injector class
"""

from src.component import Component
from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_types.fault import Fault
from src.event_bus.event import EventType

class FaultInjector(Component):
    """
    Class for fault injection. Faults can be injected into the
    InterlockingController, the Spawner and the Wrapper
    """

    _faults: list[Fault] = []
    _callback_called: bool = True

    def __init__(self, event_bus: EventBus, priority: str):
        super().__init__(event_bus, "HIGH")

    def add_fault(self, fault: Fault):
        """Adds faults that should be injected to the fault injector

        :param json_faults: The list of faults as JSON objects
        :type json_faults: list[str]
        """
        self._faults.append(fault)

    def inject_dependent_fault(self, event):
        for fault in self._faults:
            if fault.configuration.description == "test ScheduleBlockedFault" and not self._callback_called:
                self._callback_called = True
                fault.inject_fault(520)


    def next_tick(self, tick: int):
        """Called by the wrapper to announce the next tick of the simulation

        :param tick: The current simulation tick
        :type tick: int
        """

        for fault in self._faults:
            if fault.configuration.description == "test ScheduleBlockedFault":
                self.event_bus.register_callback(self.inject_dependent_fault, EventType.INJECT_FAULT)

        for fault in self._faults:
            fault.next_tick(tick)
