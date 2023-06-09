import os

import pytest

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault


class TestFault:
    """Test fault"""

    class MockConfiguration(FaultConfiguration):
        """Mock configuration"""

        strategy: str = "regular"

    class MockSpecialFault(Fault):
        """Mock fault"""

        tick_injected: int = 0
        tick_resolved: int = 0

        def inject_fault(self, tick: int):
            self.tick_injected = tick

        def resolve_fault(self, tick: int):
            self.tick_resolved = tick

    @pytest.fixture
    def configuration(self):
        configuration = self.MockConfiguration()
        configuration.start_time = 3
        configuration.end_time = 30
        return configuration

    @pytest.fixture
    def fault(
        self,
        configuration,
        event_bus,
        simulation_object_updater,
        interlocking_disruptor,
    ):
        return self.MockSpecialFault(
            configuration,
            event_bus,
            simulation_object_updater,
            interlocking_disruptor,
        )

    def test_next_tick(self, fault: MockSpecialFault):
        for tick in range(3000):
            fault.next_tick(tick)
        assert int(float(fault.tick_injected) * float(os.getenv("TICK_LENGTH"))) == 3
        assert int(float(fault.tick_resolved) * float(os.getenv("TICK_LENGTH"))) == 30
