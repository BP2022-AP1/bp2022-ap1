import pytest

from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.platform_blocked_fault import PlatformBlockedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
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
    def platform(self) -> Platform:
        return Platform("fault injector platform")

    @pytest.fixture
    def combine_platform_and_wrapper(
        self, platform: Platform, wrapper: SimulationObjectUpdatingComponent
    ):
        platform.updater = wrapper
        wrapper.simulation_objects.append(platform)
        return platform, wrapper

    @pytest.fixture
    def platform_blocked_fault_configuration(self, platform: Platform):
        return PlatformBlockedFaultConfiguration.create(
            **{
                "start_tick": 20,
                "end_tick": 200,
                "description": "test PlatformBlockedFault",
                "affected_element_id": platform.identifier,
            }
        )

    @pytest.fixture
    def platform_blocked_fault(
        self,
        platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
        logger: Logger,
        wrapper: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        return PlatformBlockedFault(
            configuration=platform_blocked_fault_configuration,
            logger=logger,
            wrapper=wrapper,
            interlocking=interlocking,
        )

    def test_inject_platform_blocked_fault(
        self,
        tick,
        # combine_platform_and_wrapper is needed to combine both mentioned
        # pylint: disable-next=unused-argument
        combine_platform_and_wrapper,
        platform_blocked_fault: PlatformBlockedFault,
        platform: Platform,
    ):
        assert not platform.blocked
        with pytest.raises(NotImplementedError):
            platform_blocked_fault.inject_fault(tick)
        assert platform.blocked

    def test_resolve_platform_blocked_fault(
        self,
        tick,
        # combine_platform_and_wrapper is needed to combine both mentioned
        # pylint: disable-next=unused-argument
        combine_platform_and_wrapper,
        platform_blocked_fault: PlatformBlockedFault,
        platform: Platform,
    ):
        with pytest.raises(NotImplementedError):
            platform_blocked_fault.inject_fault(tick)
        assert platform.blocked
        with pytest.raises(NotImplementedError):
            platform_blocked_fault.resolve_fault(tick)
        assert not platform.blocked
