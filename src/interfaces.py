from enum import Enum
from typing import List, Protocol, Tuple


class ISimulationObject(Protocol):
    """An object synchronized with the simulation"""

    traci_id: str

    def update(self, updates: dict) -> None:
        """Gets called whenever a simualtion tick has happened.

        :param updates: The updated values for the synchronized properties
        """

    def add_subscriptions(self) -> int:
        """Gets called when this object is created to allow
        specification of simulator-synchronized properties.

        :return: The synchronized properties (see <https://sumo.dlr.de/pydoc/traci.constants.html>)
        """


class ISimulationNode(ISimulationObject, Protocol):
    """A point somewhere in the simulation where `ISImulationTrack`s meet"""

    position: Tuple[float, float]


class ISimulationSignal(ISimulationNode, Protocol):
    """A signal in the simulation which can either show stop or go
    (See `ISimulationSignal.State`)
    """

    class State(Enum):
        """The possible states of the signal"""

        HALT = 1
        GO = 2

    state: State


class ISimulationSwitch(ISimulationNode, Protocol):
    """A switch in the simulation which can point either left or right
    (see `ISimulationSwitch.State`)
    """

    class State(Enum):
        """The possible states of the switch"""

        LEFT = 1
        RIGHT = 2

    state: State


class ISimulationTrack(ISimulationObject, Protocol):
    """A track in the simulation where trains can drive along"""

    blocked: bool
    speed_limit: float


class ISimulationPlatform(ISimulationObject, Protocol):
    """A platform where trains can arrive, load and unload passengers and depart"""

    track: ISimulationTrack
    station_name: str
    platform_number: int
    blocked: bool


class ISimulationTrain(ISimulationObject, Protocol):
    """A train driving around in the simulation."""

    current_track: ISimulationTrack
    priority: int
    position: Tuple[float, float]
    speed: float
    max_speed: float
    route: str
    timetable: List[ISimulationPlatform]
    _train_type: str

    def __init__(
        self,
        timetable: List[ISimulationPlatform] = None,
        train_type: str = None,
        from_simulator: bool = False,
    ):
        """Creates a new train from the given parameters.
        When initializing manually, `timetable` and `train_type` are mandatory

        :param timetable: The stations which the train should drive along,
        in the correct order. Mandatory when initializing the train yourself.
        :param train_type: The type of the train (as a SUMO VEHICLE_TYPE).
        Mandatory when initializing the train yourself.
        :param from_simulator: Specifies if train is created by the simulation or manually.
        You probably don't need to touch this.
        """
