from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrainCancelledFault(Fault):
    """A fault that blocks a platform"""

    end_tick: int = -1

    @classmethod
    def from_json(cls, json_object: str) -> "TrainCancelledFault":
        """Constructs a TrainCancelledFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a TrainCancelledFault
        :rtype: TrainCancelledFault
        """
        raise NotImplementedError()

    def inject_fault(self, component: Component):
        """inject TrainCancelledFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train by id
        # - mark train as cancelled
        raise NotImplementedError()
