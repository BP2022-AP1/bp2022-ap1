from src.fault_injector.fault_types.fault import Fault


class TrackBlockedFault(Fault):
    """A fault that blocks a track"""

    def inject_fault(self, tick: int):
        """inject TrackBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # - get track by id
        # - mark track as blocked
        raise NotImplementedError()

    def resolve_fault(self, tick: int):
        """resolves the previously injected fault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        # - get track by id
        # - mark track as no longer blocked
        raise NotImplementedError()
