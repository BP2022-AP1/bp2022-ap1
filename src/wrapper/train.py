from simualtion_object import SimulationObject
from traci import constants, vehicle
from enum import Enum
from typing import List, Protocol, Tuple


class Train(SimulationObject):
    """A train driving around in the simulation."""

    _position: Tuple(str, str) = None
    _route: str = None
    _track: Track = None
    _vehicle_type: str = None
    _speed: float = None
    _max_speed: float = None
    timetable: List[Platform] = None

    @property
    def track(self) -> Track:
        """Returns the current track the train is on

        :return: _description_
        """
        return self._track

    @property
    def position(self):
        return self._position

    @property
    def speed(self):
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
        return self._max_speed

    @max_speed.setter
    def max_speed(self, speed) -> None:
        vehicle.setMaxSpeed(self.traci_id, speed)
        self._max_speed = speed

    def __init__(
        self,
        identifier: str = None,
        timetable: List[Platform] = None,
        train_type: str = None,
        from_simulator: bool = False,
    ):
        """Creates a new train from the given parameters.
        When initializing manually, `timetable` and `train_type` are mandatory
        :param identifier: 
        :param timetable: The stations which the train should drive along,
        in the correct order. Mandatory when initializing the train yourself.
        :param train_type: The type of the train (as a SUMO VEHICLE_TYPE).
        Mandatory when initializing the train yourself.
        :param from_simulator: Specifies if train is created by the simulation or manually.
        You probably don't need to touch this.
        """
        SimulationObject.__init__(self, *args, **kwargs)

    def _add_to_simulation(self, timetable: List[Platform], train_type: str):
        vehicle.add("asdf", route_id, vehicle_type)

    def update(self, updates: dict):
        """Gets called whenever a simualtion tick has happened.
        :param updates: The updated values for the synchronized properties
        """
        self._position = updates[constants.VAR_POSITION]
        self._track_id = updates[constants.VAR_ROAD_ID]
        self._route = updates[constants.VAR_ROUTE]
        self._speed = updates[constants.VAR_SPEED]
        self._max_speed = updates[constants.VAR_MAXSPEED]

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


class Node(SimulationObject):
    """A point somewhere in the simulation where `ISImulationTrack`s meet"""

    pass


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
