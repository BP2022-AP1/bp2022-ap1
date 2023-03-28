from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrainPrioFault(Fault):
    """A fault affecting the priority of trains."""

    new_prio: int = None
    old_prio: int = None

    @classmethod
    def from_json(cls, json_object: str) -> "TrainPrioFault":
        """Constructs a TrainPrioFault from a JSON object

        :param json_object: The JSON object
        :type json_object: str
        :return: a TrainPrioFault
        :rtype: TrainPrioFault
        """
        raise NotImplementedError()

    def inject_fault(self, component: Component):
        """inject TrainPrioFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train object
        # - save the current prio of the train in old_prio
        # - set train prio to new_prio
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        # - get train object
        # - set the train prio to old_prio

        raise NotImplementedError()
