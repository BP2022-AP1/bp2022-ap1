from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrainCancelledFault(Fault):
    """A fault that blocks a platform"""

    end_tick: int = -1

    def inject_fault(self, component: Component):
        """inject TrainCancelledFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train by id
        # - mark train as cancelled
        raise NotImplementedError()
