from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

from traci import constants, vehicle, trafficlight


class SimulationObject(ABC):
    """This class represents an object inside the sumo simulation.
    It is updated every simulation tick using the update method
    and can manipulate the simualtion directly.
    """

    identifier = None
    _updater = None

    def __init__(self, identifier=None):
        self.identifier = identifier

    @updater.setter
    def updater(self, updater: "SimulationObjectUpdatingComponent"):
        self._updater = updater

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


class Switch(Node):
    """A switch in the simulation which can point either left or right
    (see `ISimulationSwitch.State`)
    """

    class State(Enum):
        """The possible states of the switch"""

        LEFT = 1
        RIGHT = 2

    state: State


class Track(SimulationObject):
    """A track in the simulation where trains can drive along"""

    blocked: bool
    speed_limit: float


class Platform(SimulationObject):
    """A platform where trains can arrive, load and unload passengers and depart"""

    track: Track
    station_name: str
    platform_number: int
    blocked: bool


class Train(SimulationObject):
    """A train driving around in the simulation."""

    # pylint: disable=too-many-instance-attributes

    _position: Tuple[float, float] = None
    _route: str = None
    _track: Track = None
    _vehicle_type: str = None
    _speed: float = None
    _max_speed: float = None
    _priority: int = None
    _train_type: str = None
    _timetable: List[Platform] = None

    @property
    def track(self) -> Track:
        """Returns the current track the train is on

        :return: _description_
        """
        return self._track

    @property
    def position(self) -> Tuple[float, float]:
        """The position of the train.
        performance impact: This method doesn't perform a traci call.

        :return: The position of the train
        """
        return self._position

    @property
    def speed(self) -> float:
        """The current speed of the train
        performance impact: This method doesn't perform a traci call.

        :return: The train-speed
        """
        return self._speed

    @property
    def route(self) -> str:
        """This method returns the current sumo-route-id.

        :return: The route this vehicle is following
        """
        return self._route

    @route.setter
    def route(self, route_id: str) -> None:
        """This method updates the vehicle route to the given sumo-route.

        :performance consideration: This method makes one traci-roundtrip
        :param route: the route that the vehicle should follow
        """
        vehicle.setRouteID(self.identifier, route_id)
        self._route = route_id

    @property
    def max_speed(self) -> float:
        """Returns the maximum speed of the train (m/s).
        performance impact: This method does not call traci.

        :return: The top speed (see
        <https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getMaxSpeed>)
        """
        return self._max_speed

    @max_speed.setter
    def max_speed(self, speed: float) -> None:
        """Updates the maximum speed to the given value (m/s).
        performance impact: This method calls traci.

        :param speed: The new top speed (see
        <https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-setMaxSpeed>)
        """
        vehicle.setMaxSpeed(self.identifier, speed)
        self._max_speed = speed

    @property
    def priority(self) -> int:
        """Returns the priority for this train (higher number means higher priority)

        :return: The train priority
        """
        return self._priority

    @priority.setter
    def priority(self, priority: int) -> None:
        """Sets the priority of this train (higher number means higher priority)

        :param priority: The new train priority
        """
        self._priority = priority

    @property
    def train_type(self) -> str:
        """Returns the train type.

        :return: The SUMO-type of the train
        """
        return self._train_type

    @property
    def timetable(self) -> List[Platform]:
        """Returns the timetable of the train

        :return: the timetable of the train
        """
        return self._timetable

    @timetable.setter
    def timetable(self, timetable: List[Platform]) -> None:
        """Updates the timetable of this train to the given timetable

        :param timetable: the new timetable
        """
        self._timetable = timetable

    def __init__(
        self,
        identifier: str = None,
        timetable: List[str] = None,
        train_type: str = None,
        priority: int = 0,
        from_simulator: bool = False,
    ):  # pylint: disable=too-many-arguments
        """Creates a new train from the given parameters.
        When initializing manually, `timetable` and `train_type` are mandatory
        :param identifier: The identifier of the train
        :param timetable: The stations which the train should drive along,
        in the correct order. Mandatory when initializing the train yourself.
        :param train_type: The type of the train (as a SUMO VEHICLE_TYPE).
        Mandatory when initializing the train yourself.
        :param priority: The priority of the train (higher number means higher priority)
        :param from_simulator: Specifies if train is created by the simulation or manually.
        You probably don't need to touch this.
        """
        SimulationObject.__init__(self, identifier=identifier)

        self._priority = priority
        self._train_type = train_type
        self._convert_timetable(timetable)

        if not from_simulator:
            self._add_to_simulation(identifier, timetable, train_type)

    def _convert_timetable(self, timetable: List[str]):
        converted = []
        for item in timetable:
            converted.append(
                next(x for x in self._updater.platforms if x.identifier == item)
            )

        self._timetable = converted

    def _add_to_simulation(
        self, identifier: str, timetable: List[Platform], train_type: str
    ):
        self._timetable = timetable
        route = "not-implemented"  # TODO: fetch the first route from the list of platforms #pylint: disable=fixme
        vehicle.add(identifier, route, train_type)

    def update(self, data: dict):
        """Gets called whenever a simualtion tick has happened.
        :param updates: The updated values for the synchronized properties
        """
        self._position = data[constants.VAR_POSITION]
        self._track = data[constants.VAR_ROAD_ID]
        self._route = data[constants.VAR_ROUTE]
        self._speed = data[constants.VAR_SPEED]
        self._max_speed = data[constants.VAR_MAXSPEED]

    def add_subscriptions(self) -> int:
        """Gets called when this object is created to allow
        specification of simulator-synchronized properties.
        :return: The synchronized properties (see <https://sumo.dlr.de/pydoc/traci.constants.html>)
        """
        return (
            constants.VAR_POSITION
            + constants.VAR_ROUTE
            + constants.VAR_ROAD_ID
            + constants.VAR_SPEED
            + constants.VAR_MAXSPEED
        )
