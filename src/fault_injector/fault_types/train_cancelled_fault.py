from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfig


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
    

class TrainCancelledFaultConfig(FaultConfig):
    """Class that contains the attributes of the TrainCancelledFault class"""

    end_tick: int = -1
