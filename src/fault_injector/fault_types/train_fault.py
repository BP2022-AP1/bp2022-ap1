from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrainFault(Fault):
    """A fault affecting trains."""

    @classmethod
    def from_json(cls, json_object: str) -> "Fault":
        """Constructs a TrainFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a TrainFault
        :rtype: Fault
        """
        raise NotImplementedError()

    def inject_fault(component: Component):
        """inject TrainFault into the given component

        :param component: _description_
        :type component: Component
        """

        raise NotImplementedError()
