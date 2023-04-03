from enum import Enum
from typing import List, Tuple

from traci import constants, vehicle

from src.wrapper.simulation_object import SimulationObject


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

    state: State


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

    _position: Tuple(str, str) = None
    _route: str = None
    _track: Track = None
    _vehicle_type: str = None
    _speed: float = None
    _max_speed: float = None
    _priority: int = None
    _train_type: str = None
    timetable: List[Platform] = None

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
    def route(self) -> int:
        """This method returns the current sumo-route-id.

        :return: The route this vehicle is following
        """
        return self._route

    @route.setter
    def route(self, route: int) -> None:
        """This method updates the vehicle route to the given sumo-route.

        :performance consideration: This method makes one traci-roundtrip
        :param route: the route that the vehicle should follow
        """
        vehicle.setRouteID(self.traci_id, route)
        self._route = route

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
        vehicle.setMaxSpeed(self.traci_id, speed)
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

    def __init__(
        self,
        identifier: str = None,
        timetable: List[Platform] = None,
        train_type: str = None,
        from_simulator: bool = False,
    ):
        """Creates a new train from the given parameters.
        When initializing manually, `timetable` and `train_type` are mandatory
        :param identifier: The identifier of the train
        :param timetable: The stations which the train should drive along,
        in the correct order. Mandatory when initializing the train yourself.
        :param train_type: The type of the train (as a SUMO VEHICLE_TYPE).
        Mandatory when initializing the train yourself.
        :param from_simulator: Specifies if train is created by the simulation or manually.
        You probably don't need to touch this.
        """
        SimulationObject.__init__(self)

        self._train_type = train_type

        if from_simulator:
            self._add_to_simulation(identifier, timetable, train_type)

    def _add_to_simulation(
        self, identifier: str, timetable: List[Platform], train_type: str
    ):
        route = str(timetable)  # TODO: fetch the first route from the list of platforms
        vehicle.add(identifier, route, train_type)

    def update(self, data: dict):
        """Gets called whenever a simualtion tick has happened.
        :param updates: The updated values for the synchronized properties
        """
        self._position = data[constants.VAR_POSITION]
        self._track = data[
            constants.VAR_ROAD_ID
        ]  # TODO: fetch the track from the list of tracks
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
