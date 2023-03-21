from abc import ABC, abstractmethod
from src.component import Component


class Fault(ABC):
    """An abstract fault for the fault injection"""

    @classmethod
    @abstractmethod
    def from_json(cls, json_object: str) -> "Fault":
        """constructs an fault object from a JSON object

        :param json_object: a json object containing the relevant info for the fault
        :type json_object: string
        :return: a fault
        :rtype: Fault
        """

        raise NotImplementedError()

    @abstractmethod
    def inject_fault(component: Component):
        """injects the fault into the given component

        :param component: the component the fault should be injected into
        :type component: Component
        """

        raise NotImplementedError()
