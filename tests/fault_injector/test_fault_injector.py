import pytest

from src.fault_injector.fault_injector import FaultInjector
from src.fault_injector.fault_types.fault import Fault
from src.fault_injector.fault_types.platform_blocked_fault import PlatformBlockedFault
from src.fault_injector.fault_types.track_blocked_fault import TrackBlockedFault


class TestFaultInjector:
    """tests the method of the fault injector component"""

    class MockFault:
        received_ticks: int = 0
        last_tick: int

        def next_tick(self, tick: int):
            self.received_ticks += 1
            self.last_tick = tick

    @pytest.fixture
    def fault_1(self):
        return self.MockFault()

    @pytest.fixture
    def fault_2(self):
        return self.MockFault()

    @pytest.fixture
    def fault_injector(self, event_bus) -> FaultInjector:
        return FaultInjector(event_bus=event_bus, priority=1)

    def test_add_fault(
        self, fault_injector: FaultInjector, fault_1: MockFault, fault_2: MockFault
    ):
        assert len(fault_injector._faults) == 0
        fault_injector.add_fault(fault_1)
        assert len(fault_injector._faults) == 1
        fault_injector.add_fault(fault_2)
        assert len(fault_injector._faults) == 2
        assert fault_1 in fault_injector._faults
        assert fault_2 in fault_injector._faults

    def test_next_tick(
        self, fault_injector: FaultInjector, fault_1: MockFault, fault_2: MockFault
    ):
        fault_injector._faults += [fault_1, fault_2]
        fault_2.next_tick(0)
        for i in range(0, 10):
            fault_injector.next_tick(i)
            assert fault_1.received_ticks == fault_2.received_ticks - 1 == i + 1
            assert fault_1.last_tick == fault_2.last_tick == i
