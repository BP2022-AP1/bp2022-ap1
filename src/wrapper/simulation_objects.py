from abc import ABC, abstractmethod
from enum import Enum

from traci import trafficlight


class SimulationObject(ABC):
    """This class represents an object inside the sumo simulation.
    It is updated every simulation tick using the update method
    and can manipulate the simualtion directly.
    """

    identifier = None

    def __init__(self, identifier=None):
        self.identifier = identifier

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


class Node(SimulationObject):
    """A point somewhere in the simulation where `Track`s meet"""


class Signal(Node):
    """A signal in the simulation which can either show stop or go
    (See `ISimulationSignal.State`)
    """

    class State(Enum):
        """The possible states of the signal"""

        HALT = 1
        GO = 2

    _state: "Signal.State"

    @property
    def state(self) -> "Signal.State":
        """Returns the current state of the signal
        performance impact: this method does not call traci

        :return: the current signal state (see `Signal.State`)
        """
        return self._state

    @state.setter
    def state(self, target: "Signal.State") -> None:
        """Updates the signal state to the given state.
        performance impact: this method calls traci every time.
        See <https://sumo.dlr.de/pydoc/traci._trafficlight.html>

        :param target: the target signal state
        """
        if target is Signal.State.HALT:
            trafficlight.setRedYellowGreenState(self.identifier, "rr")
        elif target is Signal.State.GO:
            trafficlight.setRedYellowGreenState(self.identifier, "GG")

        self._state = target

    def __init__(self, identifier: str = None, state: "Signal.State" = State.HALT):
        Node.__init__(self, identifier)
        self.state = state

    def update(self, data: dict):
        return

    def add_subscriptions(self) -> int:
        return 0
