import pytest

from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)


class TestPlatformBlockedFaultConfiguration:
    """
    tests the creation, serialization and deserialization of the PlatformBlockedFaultConfiguration
    """

    @pytest.fixture
    def start_tick(self):
        return 1

    @pytest.fixture
    def end_tick(self):
        return 3

    @pytest.fixture
    def description(self):
        return "PlatformBlockedFault"

    @pytest.fixture
    def affected_element_id(self):
        return "12345678"

    @pytest.fixture
    def fault_as_dict(self, start_tick, end_tick, description, affected_element_id):
        return {
            "start_tick": start_tick,
            "end_tick": end_tick,
            "description": description,
            "affected_element_id": affected_element_id,
        }

    @pytest.fixture
    def empty_fault_as_dict(self):
        return {}
