from abc import ABC, abstractmethod


class SimulationObject(ABC):
    """This class represents an object inside the sumo simulation.
    It is updated every simulation tick using the update method
    and can manipulate the simualtion directly.
    """

    traci_id = None

    def __init__(self, traci_id=None):
        self.traci_id = traci_id

    @abstractmethod
    def update(self, data: dict):
        """This method will be called after every sumo tick to update the traci-object

        :param data: The update from traci (the result from a subscription)
        """
        raise NotImplementedError()

    @abstractmethod
    def add_subscriptions(self):
        """This method will be called when the object enters
        the simulation to add the corresponding traci-supscriptions.
        The return value should be compatible with
         the xxx in the following call `traci.subscribe(self._id, xxx)`.
        See <https://sumo.dlr.de/pydoc/traci.domain.html#Domain-subscribe>.
        """
        raise NotImplementedError()
