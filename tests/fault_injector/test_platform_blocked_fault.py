import pytest

from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.platform_blocked_fault import PlatformBlockedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Platform
from tests.decorators import recreate_db_setup


class TestPlatformBlockedFault:
    """Tests for PlatformBlockedFault"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def platform_blocked_fault_configuration(self, basic_platform: Platform):
        return PlatformBlockedFaultConfiguration.create(
            **{
                "start_time": 20,
                "end_time": 200,
                "description": "test PlatformBlockedFault",
                "affected_element_id": basic_platform.identifier,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def platform_blocked_fault(
        self,
        platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
        event_bus: EventBus,
        souc: SimulationObjectUpdatingComponent,
        interlocking_disruptor: IInterlockingDisruptor,
    ):
        return PlatformBlockedFault(
            configuration=platform_blocked_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=souc,
            interlocking_disruptor=interlocking_disruptor,
        )

    def test_inject_platform_blocked_fault(
        self,
        tick,
        platform_blocked_fault: PlatformBlockedFault,
        basic_platform: Platform,
    ):
        assert not basic_platform.blocked
        platform_blocked_fault.inject_fault(tick)
        assert (
            platform_blocked_fault.interlocking_disruptor.route_controller.method_calls
            == 1
        )
        assert basic_platform.blocked

    def test_resolve_platform_blocked_fault(
        self,
        tick,
        platform_blocked_fault: PlatformBlockedFault,
        basic_platform: Platform,
    ):
        platform_blocked_fault.inject_fault(tick)
        assert basic_platform.blocked
        assert (
            platform_blocked_fault.interlocking_disruptor.route_controller.method_calls
            == 1
        )
        platform_blocked_fault.resolve_fault(tick)
        assert (
            platform_blocked_fault.interlocking_disruptor.route_controller.method_calls
            == 2
        )
        assert not basic_platform.blocked
