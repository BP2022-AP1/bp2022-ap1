from src.fault_injector.fault_types.fault import Fault


class PlatformBlockedFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self, tick: int):
        """inject PlatformBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # - get platform by id
        # - mark platform as blocked
        raise NotImplementedError()

    def resolve_fault(self, tick: int):
        """resolve the PlatformBlockedFault that was previously injected into the given component

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        # - get platform by id
        # - mark platform as no longer blocked
        raise NotImplementedError()
