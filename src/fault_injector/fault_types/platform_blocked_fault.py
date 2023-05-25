from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.wrapper.simulation_objects import Platform


class PlatformBlockedFault(Fault):
    """A fault that blocks a platform"""

    configuration: PlatformBlockedFaultConfiguration
    platform: Platform = None

    def _get_platform(self) -> Platform:
        platforms: list[Platform] = [
            platform
            for platform in self.simulation_object_updater.platforms
            if platform.identifier == self.configuration.affected_element_id
        ]
        if len(platforms) < 1:
            raise ValueError("platform does not exist")
        return platforms[0]

    def inject_fault(self, tick: int):
        """inject PlatformBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.platform: Platform = self._get_platform()
        self.platform.blocked = True

        self.interlocking.insert_platform_blocked(self.platform)
        self.event_bus.inject_platform_blocked_fault(
            tick, self.configuration.id, self.platform.identifier
        )

    def resolve_fault(self, tick: int):
        """resolve the PlatformBlockedFault that was previously injected into the given component

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        if self.platform is None:
            raise ValueError("Fault not injected")

        self.platform.blocked = False
        self.interlocking.insert_platform_unblocked(self.platform)
        self.event_bus.resolve_platform_blocked_fault(tick, self.configuration.id)
