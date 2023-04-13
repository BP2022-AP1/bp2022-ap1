from src.fault_injector.fault_types.fault import Fault


class ScheduleBlockedFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self, tick: int):
        """inject ScheduleBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # - get schedule by id
        # - mark schedule as blocked
        raise NotImplementedError()

    def resolve_fault(self, tick: int):
        """resolves the previously injected ScheduleBlockedFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        raise NotImplementedError()
