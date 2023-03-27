from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrainSpeedFault(Fault):
    """A fault affecting the speed of trains."""

    @classmethod
    def from_json(cls, json_object: str) -> "TrainSpeedFault":
        """Constructs a TrainFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a TrainFault
        :rtype: TrainFault
        """
        raise NotImplementedError()

    def inject_fault(component: Component):
        """inject TrainFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        raise NotImplementedError()
