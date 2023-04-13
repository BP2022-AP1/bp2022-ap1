from src.fault_injector.fault_types.fault import Fault


class TrainPrioFault(Fault):
    """A fault affecting the priority of trains."""

    def inject_fault(self, tick: int):
        """inject TrainPrioFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # - get train object
        # - save the current prio of the train in old_prio
        # - set train prio to new_prio
        raise NotImplementedError()

    def resolve_fault(self, tick: int):
        """resolves the previously injected TrainPrioFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        # - get train object
        # - set the train prio to old_prio

        raise NotImplementedError()
