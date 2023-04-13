from src.fault_injector.fault_types.fault import Fault


class TrainCancelledFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self, tick: int):
        """inject TrainCancelledFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # - get train by id
        # - mark train as cancelled
        raise NotImplementedError()

    def resolve_fault(self, tick: int):
        """resolves the previously injected TrainCancelledFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        raise NotImplementedError()
