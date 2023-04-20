from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.wrapper.simulation_objects import Platform


class PlatformBlockedFault(Fault):
    """A fault that blocks a platform"""

    configuration: PlatformBlockedFaultConfiguration
    platform: Platform

    def inject_fault(self, tick: int):
        """inject PlatformBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.platform: Platform = [
            platform
            for platform in self.wrapper.platforms
            if platform.identifier == self.configuration.affected_element_id
        ][0]
        self.platform.blocked = True

        self.interlocking.insert_platform_blocked(self.platform.identifier)
        self.logger.inject_platform_blocked_fault(
            tick, self.configuration.id, self.platform.identifier
        )

    def resolve_fault(self, tick: int):
        """resolve the PlatformBlockedFault that was previously injected into the given component

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        if self.platform is None:
            raise ValueError(
                "Platform not set, probably due to not injecting the fault"
            )
        self.platform.blocked = False

        self.interlocking.insert_platform_unblocked(self.platform.identifier)

        self.logger.resolve_platform_blocked_fault(tick, self.configuration.id)
