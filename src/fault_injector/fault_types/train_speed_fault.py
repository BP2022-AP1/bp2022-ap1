from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfig


class TrainSpeedFault(Fault):
    """A fault affecting the speed of trains."""

    def inject_fault(self, component: Component):
        """inject TrainSpeedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train object
        # - save the current speed of the train in old_speed
        # - set train speed to new_speed
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        # - get train object
        # - set the train speed to old_speed

        raise NotImplementedError()
