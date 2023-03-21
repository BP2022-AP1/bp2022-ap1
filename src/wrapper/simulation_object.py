from abc import ABC, abstractmethod
import traci

class SimulationObject(ABC):
    self._id = None

    def __init__(self, traci_id = None):
        self._id = traci_id

    @abstractmethod
    def _update(self, data: dict):
        """This method will be called after every sumo tick to update the traci-object

        :param data: The update from traci (the result from a subscription)
        """
        raise NotImplementedError()

    @abstractmethod
    def _add_subscriptions(self):
        """This method will be called when the object enters the simulation to add the corresponding traci-supscriptions.
        The return value should be compatible with the xxx in the following call `traci.subscribe(self._id, xxx)`.
        See <https://sumo.dlr.de/pydoc/traci.domain.html#Domain-subscribe>.
        """
        raise NotImplementedError()