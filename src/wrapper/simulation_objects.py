from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

from sumolib import net
from traci import constants, edge, trafficlight, vehicle


class SimulationObject(ABC):
    """This class represents an object inside the sumo simulation.
    It is updated every simulation tick using the update method
    and can manipulate the simualtion directly.
    """

    identifier: str = None
    updater: "SimulationObjectUpdatingComponent" = None

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

    @staticmethod
    @abstractmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> "SimulationObject":
        """This method is called to initialize the object from the simulator.
        When using SUMO, the simulation will not be started when this method is called.

        :param simulation_object: The simulation object to initialize this object from.
        """
        raise NotImplementedError()

    @abstractmethod
    def add_simulation_connections(self) -> None:
        """This method is called, when all other simulation-connected objects are initialized.
        You can establish links between objects in this method (e.g. between two edges).

        When this method is called, the simulation is still not started,
        but you have access to all the other simulation objects via `self.updater`.
        """
        raise NotImplementedError()


class Node(SimulationObject):
    """A point somewhere in the simulation where `Track`s meet"""

    _edges: List["Edge"] = None
    _edge_ids: List["str"] = None

    @property
    def edges(self) -> List["Edge"]:
        """Returns the edges this node is connected to

        :return: The connected edges
        """

        return self._edges

    def update(self, data: dict):
        pass

    def add_subscriptions(self):
        pass

    def set_edges(self, simulation_object: net.node) -> None:
        """Sets the edges that are connected to this node

        :param simulation_object: the current node as a sumo net.node
        """
        self._edge_ids = [
            edge.getID()
            for edge in simulation_object.getOutgoing()
            + simulation_object.getIncoming()
        ]

    @staticmethod
    def from_simulation(
        simulation_object: net.node, updater: "SimulationObjectUpdatingComponent"
    ) -> "SimulationObject":
        if simulation_object.getID() in [x.identifier for x in updater.signals]:
            # We need to update the signal with our data
            signal: "Signal" = [
                signal
                for signal in updater.signals
                if signal.identifier == simulation_object.getID()
            ][0]

            signal.add_edges(simulation_object)

            return None

        # we need to create a new node

        result = Node(identifier=simulation_object.getID())
        result.updater = updater
        result.set_edges(simulation_object)

        return result

    def add_simulation_connections(self) -> None:
        self._edges = [x for x in self.updater.edges if x.identifier in self._edge_ids]


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
        super().__init__(identifier=identifier)
        self.state = state

    def update(self, data: dict):
        return

    def add_subscriptions(self) -> int:
        return 0

    def set_edges(self, simulation_object: net.TLS) -> None:
        self._edge_ids = [edge.getID() for edge in simulation_object.getEdges()]

    def add_edges(self, node: net.node) -> None:
        """Adds more edges to the signal (coming from the passed node)

        :param node: The node from which to load the additional edges
        """
        assert node.getID() == self.identifier

        self._edge_ids += [
            edge.getID() for edge in node.getOutgoing() + node.getIncoming()
        ]

    @staticmethod
    def from_simulation(
        simulation_object: net.TLS, updater: "SimulationObjectUpdatingComponent"
    ) -> "Signal":
        result = Signal(identifier=simulation_object.getID())
        result.updater = updater
        result.set_edges(simulation_object)

        return result


class Switch(Node):
    """A switch in the simulation which can point either left or right
    (see `ISimulationSwitch.State`)
    """

    class State(Enum):
        """The possible states of the switch"""

        LEFT = 1
        RIGHT = 2

    _state: "Switch.State"

    def __init__(self, identifier: str = None):
        super().__init__(identifier)
        self._state = Switch.State.LEFT

    @property
    def state(self) -> State:
        """Returns current state of the switch
        (the state is only local as SUMO doesn't consider the switch state)

        :return: The switch state
        """
        return self._state

    @state.setter
    def state(self, target) -> None:
        """Updates the state of the switch

        :param target: The new state
        :raises ValueError: Thrown when you are trying to set the state to an invalid state
        """
        if target not in (Switch.State.LEFT, Switch.State.RIGHT):
            raise ValueError("Wrong target state")

        self._state = target

    def update(self, data: dict) -> None:
        return  # We don't have to update anything from the simulator

    def add_subscriptions(self) -> int:
        return 0  # We don't have to update anything from the simulator

    @staticmethod
    def from_simulation(
        simulation_object: net.node, updater: "SimulationObjectUpdatingComponent"
    ) -> "Switch":
        # see: https://sumo.dlr.de/pydoc/sumolib.net.node.html
        result = Switch(identifier=simulation_object.getID())
        result.updater = updater
        result.set_edges(simulation_object)

        return result


class Edge(SimulationObject):
    """A track in the simulation where trains can drive along, only in one direction"""

    blocked: bool
    _max_speed: float
    _track: "Track" = None
    _from: Node | str = None
    _to: Node | str = None

    @property
    def to_node(self) -> Node:
        """The node which is it at the end of the edge

        :return: The end-node
        """
        assert not isinstance(self._to, str)

        return self._to

    @property
    def from_node(self) -> Node:
        """The node which is at the beginning of the edge

        :return: The start-node
        """
        assert not isinstance(self._from, str)

        return self._from

    @property
    def max_speed(self) -> float:
        """The current maximum speed of the track

        :return: the speed in m/s
        """
        return self._max_speed

    @property
    def track(self) -> "Track":
        """Returns the track which this edge is part of

        :return: The track
        """
        return self._track

    @track.setter
    def track(self, track: "Track") -> None:
        """Updates the edge to contain the parent Track

        :param track: The track this edge belongs to
        """
        assert self._track is None and track is not None
        self._track = track

    @max_speed.setter
    def max_speed(self, max_speed: float) -> None:
        """Updates the max_speed of the edge
        performance consideration: This method performs a traci call

        :param max_speed: The new maximum speed of the edge
        """
        edge.setMaxSpeed(self.identifier, max_speed)
        self._max_speed = max_speed

    def __init__(self, identifier: str = None):
        super().__init__(identifier)
        self.blocked = False

    def update(self, data: dict):
        self._max_speed = data[constants.VAR_MAXSPEED]

    def add_subscriptions(self) -> int:
        return constants.VAR_MAXSPEED

    @staticmethod
    def from_simulation(simulation_object: net.edge, updater) -> "Track":
        # see: https://sumo.dlr.de/pydoc/sumolib.net.edge.html
        result = Edge(simulation_object.getID())
        result.updater = updater

        # pylint: disable=protected-access
        result._from = simulation_object.getFromNode().getID()
        result._to = simulation_object.getToNode().getID()

        return result

    def add_simulation_connections(self) -> None:
        self._from = [
            node for node in self.updater.nodes if node.identifier == self._from
        ][0]
        self._to = [node for node in self.updater.nodes if node.identifier == self._to][
            0
        ]


class Track(SimulationObject):
    "A track on which trains can drive both directions"

    _edges = Tuple[Edge, Edge]

    @property
    def edges(self) -> Tuple[Edge, Edge]:
        """Returns the edges represented by this track

        :return: The edges in both directions
        """
        return self._edges

    @property
    def nodes(self) -> Tuple[Node, Node]:
        """Returns the nodes the edges run between

        :return: The nodes
        """
        return (self._edges[0].from_node, self._edges[0].to_node)

    def __init__(self, edge1, edge2):
        if edge1.identifier.endswith("-re"):
            assert edge1.identifier.split("-re")[0] == edge2.identifier
            self._edges = (edge1, edge2)
        else:
            assert edge1.identifier == edge2.identifier.split("-re")[0]
            self._edges = (edge2, edge1)

        super().__init__(identifier=self._edges[0].identifier)

        edge1.track = self
        edge2.track = self

    @property
    def max_speed(self) -> Tuple[float, float] | float:
        """Returns the max_speed of the track

        :return: If both edges have the same speed, a float is returned,
        if the edges have different speeds, a tuple is returned
        """
        speed0 = self.edges[0].max_speed
        speed1 = self.edges[1].max_speed

        if speed0 == speed1:
            return speed0

        return (speed0, speed1)

    @max_speed.setter
    def max_speed(self, speed: Tuple[float, float] | float) -> None:
        """Updates the max_speed of the track

        :param speed: If both edges should have the same speed, a floatshould be passed,
        if the edges should have different speeds, pass a tuple
        """
        if not isinstance(speed, Tuple):
            speed = (speed, speed)

        self.edges[0].max_speed = speed[0]
        self.edges[1].max_speed = speed[1]

    @property
    def blocked(self) -> Tuple[bool, bool] | bool:
        """Returns if the edge/track is blocked.

        :return: If only one edge is blocked, a tuple is returned;
        if both edges are blocked / unblocked, a plain bool is returned
        """
        if self.edges[0].blocked == self.edges[1].blocked:
            return self.edges[0].blocked
        return (self.edges[0].blocked, self.edges[1].blocked)

    @blocked.setter
    def blocked(self, blocked: Tuple[bool, bool] | bool) -> None:
        """Block the edges represented by this track

        :param blocked: Which edge to block (if only one direction should be blocked,
        use the tuple, else use the plain bool)
        """
        if not isinstance(blocked, Tuple):
            blocked = (blocked, blocked)

        self.edges[0].blocked = blocked[0]
        self.edges[1].blocked = blocked[1]

    def update(self, data: dict) -> None:
        # pylint: disable=unused-argument
        pass

    def add_subscriptions(self):
        pass

    @staticmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> "SimulationObject":
        pass

    def add_simulation_connections(self) -> None:
        pass


class Platform(SimulationObject):
    """A platform where trains can arrive, load and unload passengers and depart"""

    _edge: Edge = None
    _edge_id: str
    _platform_id: str
    blocked: bool

    @property
    def track(self) -> Track:
        return self.edge.track

    @property
    def edge(self) -> Edge:
        """The track on which the stop is located

        :return: The track
        """
        if self._edge is None or self._edge.identifier != self._edge_id:
            self._edge = next(
                item for item in self.updater.edges if item.identifier == self._edge_id
            )
        return self._edge

    @property
    def platform_id(self) -> str:
        """The platform identifier of this platform

        :return: The identifier
        """
        return self._platform_id

    def __init__(self, identifier, platform_id: str = None, edge_id=None):
        super().__init__(identifier)
        self._platform_id = platform_id
        self.blocked = False
        self._edge_id = edge_id

    def update(self, data: dict) -> None:
        return  # We don't have to update anything from the simulator

    def add_subscriptions(self) -> int:
        return 0  # We don't have to update anything from the simulator

    @staticmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> "Platform":
        result = Platform(identifier=simulation_object.id)
        result.updater = updater
        return result

    def add_simulation_connections(self) -> None:
        # Nothing to do (we dont load trains from the sim)
        pass


class Train(SimulationObject):
    """A train driving around in the simulation."""

    # pylint: disable=too-many-instance-attributes

    class TrainType(SimulationObject):
        """Metadata about a specific train"""

        _max_speed: float = None
        _priority: int = None
        _name: str = None

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
            return self._priority if self._priority is not None else 0

        @priority.setter
        def priority(self, priority: int) -> None:
            """Sets the priority of this train (higher number means higher priority)

            :param priority: The new train priority
            """
            self._priority = priority

        @property
        def name(self) -> str:
            """Returns the train type.

            :return: The SUMO-type of the train
            """
            return self._name

        @staticmethod
        def from_sumo_type(train_type: str, instance: str):
            """Creates a new train type for the given instance

            :param train_type: The sumo type of the train
            :param instance: The sumo train to which this type corresponds
            """
            return Train.TrainType(instance, name=train_type)

        def __init__(self, identifier, name=None):
            SimulationObject.__init__(self, identifier)
            self._name = name

        def update(self, data: dict) -> None:
            self._max_speed = data[constants.VAR_MAXSPEED]

        def add_subscriptions(self) -> int:
            return constants.VAR_MAXSPEED

        @staticmethod
        def from_simulation(
            simulation_object, updater: "SimulationObjectUpdatingComponent"
        ) -> "Train.TrainType":
            pass

        def add_simulation_connections(self) -> None:
            pass

    _position: Tuple[float, float]
    _route: str
    _edge: Edge = None
    _edge_id: str
    _speed: float
    _timetable: List[Platform]
    train_type: TrainType

    @property
    def edge(self) -> Edge:
        """Returns the current edge the train is on

        :return: The current track the train is on
        """
        if self._edge is None or self._edge.identifier != self._edge_id:
            self._edge = next(
                item for item in self.updater.edges if item.identifier == self._edge_id
            )
        return self._edge

    @property
    def track(self) -> Track:
        """Returns the track (bidirectional) on which the train is currently

        :return: The track the train is dirving on
        """
        return self.edge.track

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
        timetable: List[Platform] = None,
        train_type: str = None,
        updater: "SimulationObjectUpdatingComponent" = None,
        from_simulator: bool = False,
    ):
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
        self.updater = updater

        self.train_type = Train.TrainType.from_sumo_type(train_type, identifier)
        self._timetable = timetable

        if not from_simulator:
            self._add_to_simulation(identifier, timetable, train_type)

    def _add_to_simulation(self, identifier: str, train_type: str, route: str):
        vehicle.add(identifier, route, train_type)

    def update(self, data: dict):
        """Gets called whenever a simualtion tick has happened.
        :param updates: The updated values for the synchronized properties
        """
        self._position = data[constants.VAR_POSITION]
        self._edge_id = data[constants.VAR_ROAD_ID]
        self._route = data[constants.VAR_ROUTE]
        self._speed = data[constants.VAR_SPEED]

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
        )

    @staticmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> "Train":
        # Nothing to do (we dont load trains from the sim)
        pass

    def add_simulation_connections(self) -> None:
        # Nothing to do (we dont load trains from the sim)
        pass
