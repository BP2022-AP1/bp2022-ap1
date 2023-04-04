from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfiguration


class TrainCancelledFault(Fault):
    """A fault that blocks a platform"""

    def inject_fault(self, component: Component):
        """inject TrainCancelledFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train by id
        # - mark train as cancelled
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        """resolves the previously injected TrainCancelledFault

        :param component: the component with the injected fault
        :type component: Component
        """
        raise NotImplementedError()


class TrainCancelledFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrainCancelledFault class"""
