
from src.fault_injector.fault_types.fault import Fault


class TrainPrioFault(Fault):
    """A fault affecting the priority of trains."""

    def inject_fault(self):
        """inject TrainPrioFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train object
        # - save the current prio of the train in old_prio
        # - set train prio to new_prio
        raise NotImplementedError()

    def resolve_fault(self):
        """resolves the previously injected TrainPrioFault

        :param component: the component with the injected fault
        :type component: Component
        """
        # - get train object
        # - set the train prio to old_prio

        raise NotImplementedError()
