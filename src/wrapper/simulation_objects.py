from abc import ABC, abstractmethod
from collections import defaultdict
from enum import IntEnum
from typing import List, Optional, Tuple, Union

from sumolib import net
from traci import FatalTraCIError, constants, edge, trafficlight, vehicle


class SimulationObject(ABC):
    """This class represents an object inside the sumo simulation.
    It is updated every simulation tick using the update method
    and can manipulate the simualtion directly.
    """

    identifier: str
    updater: "SimulationObjectUpdatingComponent"

    def __init__(self, identifier: str):
        self.identifier = identifier

    @abstractmethod
    def update(self, data: dict):
        """This method will be called after every sumo tick to update the traci-object

        :param data: The update from traci (the result from a subscription)
        """
        raise NotImplementedError()

    @abstractmethod
    def add_subscriptions(self) -> List[int]:
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

    _edges: List["Edge"]
    _edge_ids: List["str"]

    @property
    def edges(self) -> List["Edge"]:
        """Returns the edges this node is connected to

        :return: The connected edges
        """

        return self._edges

    def update(self, data: dict):
        # pylint: disable=unused-argument
        return

    def add_subscriptions(self) -> List[int]:
        return []

    def set_edges(self, simulation_object: net.node.Node) -> None:
        """Sets the edges that are connected to this node

        :param simulation_object: the current node as a sumo net.node
        """
        self._edge_ids = [
            my_edge.getID()
            for my_edge in simulation_object.getOutgoing()
            + simulation_object.getIncoming()
        ]

    def get_edge_to(self, other_node: "Node") -> "Edge":
        """This method returns the edge between the node this is called on and the given node.

        :param other_node: The node this node is connected to
        :return: The edge between the two nodes
        :rtype: Edge
        """
        for potential_edge in self.edges:
            if potential_edge.to_node == other_node:
                return potential_edge
        raise ValueError("The two nodes are not connected.")

    def get_edges_accessible_from(self, incoming_edge: "Edge") -> List["Edge"]:
        """This method return all edges accessible from the given edge.

        :param incoming_edge: The edge from which other edges should be accessible
        :return: A list of all accessible edges
        """
        if incoming_edge not in self.edges:
            raise ValueError("The given edge is not connected to the node.")
        return self.edges

    @staticmethod
    def from_simulation(
        simulation_object: net.node.Node, updater: "SimulationObjectUpdatingComponent"
    ) -> Optional["SimulationObject"]:
        if simulation_object.getID() in [x.identifier for x in updater.signals]:
            # We need to update the signal with our data
            signal: "Signal" = [
                signal
                for signal in updater.signals
                if signal.identifier == simulation_object.getID()
            ][0]

            signal.add_edges(simulation_object)

            return None

        # We need to create a new node
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

    class State(IntEnum):
        """The possible states of the signal"""

        HALT = 1
        GO = 2

    _state: "Signal.State"
    _incoming_edge: "Edge"
    _incoming_index: int
    _controlled_lanes_count: int

    @property
    def incoming(self) -> "Edge":
        """Returns the incoming edge to the signal. The signal only applys for that edge.

        :return: The incoming edge
        """
        return self._incoming_edge

    @incoming.setter
    def incoming(self, incoming: "Edge"):
        """Updates the incomig edge.

        :param incoming: The incoming edge
        """
        self._incoming_edge = incoming

        self.set_incoming_index()

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

        target_state = "r"
        if target is Signal.State.GO:
            target_state = "G"

        trafficlight.setRedYellowGreenState(
            self.identifier,
            "G" * self._incoming_index
            + target_state
            + "G" * ((self._controlled_lanes_count - self._incoming_index) - 1),
        )

        self._state = target

    def __init__(self, identifier: str, state: "Signal.State" = State.HALT):
        super().__init__(identifier=identifier)
        self._state = state

    def update(self, data: dict):
        return

    def add_subscriptions(self) -> List[int]:
        return []

    def set_incoming_index(self):
        """This methods sets the incoming index according to the incoming edge."""
        try:
            lanes: List[str] = trafficlight.getControlledLanes(self.identifier)
            self._controlled_lanes_count = len(lanes)
            for i, lane in enumerate(lanes):
                if self._incoming_edge.identifier == lane.split("_")[0]:
                    self._incoming_index = i

            self.state = Signal.State.HALT
        except FatalTraCIError:
            return

    def set_edges(self, simulation_object: net.TLS) -> None:
        self._edge_ids = [my_edge.getID() for my_edge in simulation_object.getEdges()]

    def add_edges(self, node: net.node.Node) -> None:
        """Adds more edges to the signal (coming from the passed node)

        :param node: The node from which to load the additional edges
        """
        assert node.getID() == self.identifier

        self._edge_ids += [
            my_edge.getID() for my_edge in node.getOutgoing() + node.getIncoming()
        ]

    @staticmethod
    def from_simulation(
        simulation_object: net.TLS, updater: "SimulationObjectUpdatingComponent"
    ) -> "Signal":
        result = Signal(identifier=simulation_object.getID())
        result.updater = updater
        result.set_edges(simulation_object)

        return result

    def get_edges_accessible_from(self, incoming_edge: "Edge") -> List["Edge"]:
        edges = super().get_edges_accessible_from(incoming_edge)
        base_edge_id = incoming_edge.identifier.split("-re")[0]
        return [
            accessible_edge
            for accessible_edge in edges
            if base_edge_id not in accessible_edge.identifier
        ]


class Switch(Node):
    """A switch in the simulation which can point either left or right
    (see `ISimulationSwitch.State`)
    """

    class State(IntEnum):
        """The possible states of the switch"""

        LEFT = 1
        RIGHT = 2

    _state: "Switch.State"
    _head_ids: List[str]
    head: List["Edge"]

    def __init__(self, identifier: str):
        super().__init__(identifier)
        self._state = Switch.State.LEFT

        self._head_ids = []
        self.head = []

    @property
    def state(self) -> State:
        """Returns current state of the switch
        (the state is only local as SUMO doesn't consider the switch state)

        :return: The switch state
        """
        return self._state

    @state.setter
    def state(self, target: "Switch.State") -> None:
        """Updates the state of the switch

        :param target: The new state
        :raises ValueError: Thrown when you are trying to set the state to an invalid state
        """
        if target not in (Switch.State.LEFT, Switch.State.RIGHT):
            raise ValueError("Wrong target state")

        self._state = target

    def update(self, data: dict) -> None:
        return  # We don't have to update anything from the simulator

    def add_subscriptions(self) -> List[int]:
        return []  # We don't have to update anything from the simulator

    @staticmethod
    def from_simulation(
        simulation_object: net.node.Node, updater: "SimulationObjectUpdatingComponent"
    ) -> "Switch":
        # see: https://sumo.dlr.de/pydoc/sumolib.net.node.html
        result = Switch(identifier=simulation_object.getID())
        result.updater = updater
        result.set_edges(simulation_object)
        result.set_connections(simulation_object)
        return result

    def add_simulation_connections(self) -> None:
        super().add_simulation_connections()
        for my_edge in self.edges:
            if my_edge.identifier in self._head_ids:
                self.head.append(my_edge)

        assert len(self.head) == 2

    def is_head(self, my_edge: "Edge") -> bool:
        """This method returns, whether the given edge is connected on head of the switch.

        :param my_edge: The edge which may be connected on head
        :return: If the edge is connected on head
        """
        return my_edge in self.head

    def set_connections(self, simulation_object: "net.node.Node"):
        """This method sets which edge_ids are connected on head of the switch.
        It only sets the head_ids, as the edge objects are not yet initialized.

        :param simulation_object: The Node object from Sumo
        """
        connections = simulation_object.getConnections()

        directions_to = defaultdict(int)
        directions_from = defaultdict(int)

        for connection in connections:
            directions_to[connection.getTo().getID()] += 1
            directions_from[connection.getFrom().getID()] += 1

        for connection in connections:
            if (
                directions_to[connection.getTo().getID()] == 2
                and connection.getTo().getID() not in self._head_ids
            ):
                self._head_ids.append(connection.getTo().getID())
            if (
                directions_from[connection.getFrom().getID()] == 2
                and connection.getFrom().getID() not in self._head_ids
            ):
                self._head_ids.append(connection.getFrom().getID())

    def get_edges_accessible_from(self, incoming_edge: "Edge") -> List["Edge"]:
        if self.is_head(incoming_edge):
            return [my_edge for my_edge in self.edges if not self.is_head(my_edge)]
        if not self.is_head(incoming_edge):
            return self.head
        raise ValueError("Given edge is not connected to the switch.")


class Edge(SimulationObject):
    """A track in the simulation where trains can drive along, only in one direction"""

    blocked: bool
    _max_speed: float
    _track: "Track"
    _from: Union[Node, str]
    _to: Union[Node, str]
    _length: float

    @property
    def to_node(self) -> Node:
        """The node which is it at the end of the edge

        :return: The end-node
        """
        assert not isinstance(self._to, str)

        return self._to

    @property
    def length(self) -> float:
        """The length of this edge

        :return: The length
        """
        return self._length

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
        return self._track if hasattr(self, "_track") else None

    @track.setter
    def track(self, track: "Track") -> None:
        """Updates the edge to contain the parent Track

        :param track: The track this edge belongs to
        """
        assert track is not None and (
            not hasattr(self, "_track") or self._track.identifier == track.identifier
        )
        self._track = track

    @max_speed.setter
    def max_speed(self, max_speed: float) -> None:
        """Updates the max_speed of the edge
        performance consideration: This method performs a traci call

        :param max_speed: The new maximum speed of the edge
        """
        edge.setMaxSpeed(self.identifier, max_speed)
        self._max_speed = max_speed

    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.blocked = False

    def update(self, data: dict):
        return

    def add_subscriptions(self) -> List[int]:
        return []

    @staticmethod
    def from_simulation(simulation_object: net.edge.Edge, updater) -> "Edge":
        # see: https://sumo.dlr.de/pydoc/sumolib.net.edge.html
        result = Edge(simulation_object.getID())
        result.updater = updater

        # pylint: disable=protected-access
        result._length = simulation_object.getLength()
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
    is_reservation_track = False

    @property
    def edges(self) -> Tuple[Edge, Edge]:
        """Returns the edges represented by this track

        :return: The edges in both directions
        """
        return self._edges

    @property
    def length(self) -> float:
        """The length of the track. If the length differ, choose the shorter one

        :return: The length
        """
        return min(self._edges[0].length, self._edges[1].length)

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
    def max_speed(self) -> Union[Tuple[float, float], float]:
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
    def max_speed(self, speed: Union[Tuple[float, float], float]) -> None:
        """Updates the max_speed of the track

        :param speed: If both edges should have the same speed, a float should be passed,
        if the edges should have different speeds, pass a tuple
        """
        if not isinstance(speed, Tuple):
            speed = (speed, speed)

        self.edges[0].max_speed = speed[0]
        self.edges[1].max_speed = speed[1]

    @property
    def blocked(self) -> Union[Tuple[bool, bool], bool]:
        """Returns if the edge/track is blocked.

        :return: If only one edge is blocked, a tuple is returned;
        if both edges are blocked / unblocked, a plain bool is returned
        """
        if self.edges[0].blocked == self.edges[1].blocked:
            return self.edges[0].blocked
        return (self.edges[0].blocked, self.edges[1].blocked)

    @blocked.setter
    def blocked(self, blocked: Union[Tuple[bool, bool], bool]) -> None:
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
        return

    def add_subscriptions(self) -> List[int]:
        return []

    @staticmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> None:
        pass

    def add_simulation_connections(self) -> None:
        pass

    def should_be_reservation_track(self) -> bool:
        """Returns if this track is between two signals and should thous be a ReservationTrack.

        :return: If that is the case
        """
        for node in self.nodes:
            if isinstance(node, Switch):
                return False
            if isinstance(node, Signal) and not node.incoming in self.edges:
                return False
        return True

    def as_reservation_track(self) -> "ReservationTrack":
        """Returns a identical ReservationTrack.

        :return: The ReservationTrack
        """
        return ReservationTrack(self.edges[0], self.edges[1])


class ReservationTrack(Track):
    """A Track between two Signals, that has reservations of trains"""

    reservations: List[Tuple["Train", Edge]]
    is_reservation_track = True

    def __init__(self, edge1, edge2):
        super().__init__(edge1, edge2)
        self.reservations = []


class Platform(SimulationObject):
    """A platform where trains can arrive, load and unload passengers and depart"""

    _edge: Edge
    _edge_id: str
    _platform_id: str
    blocked: bool

    @property
    def track(self) -> Track:
        """The track the train is on

        :return: The track
        """
        return self.edge.track

    @property
    def edge(self) -> Edge:
        """The track on which the stop is located

        :return: The track
        """
        if not hasattr(self, "_edge") or self._edge.identifier != self._edge_id:
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

    def __init__(self, identifier, platform_id: str, edge_id: str):
        super().__init__(identifier)
        self._platform_id = platform_id
        self.blocked = False
        self._edge_id = edge_id

    def update(self, data: dict) -> None:
        return  # We don't have to update anything from the simulator

    def add_subscriptions(self) -> List[int]:
        return []  # We don't have to update anything from the simulator

    @staticmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> "Platform":
        result = Platform(
            identifier=simulation_object.id,
            edge_id="_".join(simulation_object.lane.split("_")[:-1]),
            platform_id=simulation_object.id,
        )
        result.updater = updater
        return result

    def add_simulation_connections(self) -> None:
        pass


class Train(SimulationObject):
    """A train driving around in the simulation."""

    # pylint: disable=too-many-instance-attributes

    class TrainType(SimulationObject):
        """Metadata about a specific train"""

        _max_speed: float
        _priority: int
        _name: str

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

        def __init__(self, identifier, name: str = None):
            SimulationObject.__init__(self, identifier)
            self._name = name

        def update(self, data: dict) -> None:
            self._max_speed = data[constants.VAR_MAXSPEED]

        def add_subscriptions(self) -> List[int]:
            return [constants.VAR_MAXSPEED]

        @staticmethod
        def from_simulation(
            simulation_object, updater: "SimulationObjectUpdatingComponent"
        ) -> None:
            pass

        def add_simulation_connections(self) -> None:
            pass

    _position: Tuple[float, float]
    _route: str
    _edge: Edge
    _speed: float
    _timetable: List[Platform]
    _station_index: int = 0
    train_type: TrainType
    reserved_tracks: List[Track]
    station_index: int = 0
    reserved_until_station_index: int = 1

    @property
    def current_platform(self) -> Optional[Platform]:
        """Returns the platform the train is heading to.
        If the train has passed all stations or the timetable is empty, return None.

        :return: The next Platform the train is headed to, or None
        if either the timetable is empty or the train is at the end of its route
        """
        if self._station_index >= len(self._timetable) or len(self.timetable) <= 0:
            return None
        return self._timetable[self._station_index]

    @property
    def edge(self) -> Edge:
        """Returns the current edge the train is on

        :return: The current track the train is on
        """
        return self._edge if hasattr(self, "_edge") else None

    @property
    def track(self) -> Track:
        """Returns the track (bidirectional) on which the train is currently
        :return: The track the train is driving on
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
        identifier: str,
        timetable: List[Platform],
        train_type: str = None,
        updater: "SimulationObjectUpdatingComponent" = None,
        from_simulator: bool = False,
        route_id: str = None,
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
        self.reserved_tracks = []

        if not from_simulator:
            self._add_to_simulation(identifier, train_type, route_id)

    def _add_to_simulation(self, identifier: str, train_type: str, route: str):
        vehicle.add(identifier, routeID=route, typeID=train_type)

    def update(self, data: dict):
        """Gets called whenever a simualtion tick has happened.
        :param updates: The updated values for the synchronized properties
        """
        self._position = data[constants.VAR_POSITION]
        edge_id = data[constants.VAR_ROAD_ID]
        # self._route = data[constants.VAR_ROUTE]
        self._speed = data[constants.VAR_SPEED]
        if (
            not hasattr(self, "_edge")
            or self._edge.identifier != edge_id
            and not edge_id[:1] == ":"
        ):
            if hasattr(self, "_edge"):
                if edge_id not in list(
                    map(lambda obj: obj.identifier, self._edge.to_node.edges)
                ):
                    raise ValueError(
                        (
                            "A Track was skipped: Old track: "
                            f"{self._edge.identifier}, new track: {edge_id}"
                        )
                    )

                self.updater.infrastructure_provider.train_drove_off_track(
                    self, self._edge
                )
            self._edge = next(
                item for item in self.updater.edges if item.identifier == edge_id
            )
            if (
                self.current_platform is not None
                and self.edge == self.current_platform.edge
            ):
                self._station_index += 1

            self.updater.infrastructure_provider.train_drove_onto_track(
                self, self._edge
            )

    def add_subscriptions(self) -> List[int]:
        """Gets called when this object is created to allow
        specification of simulator-synchronized properties.
        :return: The synchronized properties (see <https://sumo.dlr.de/pydoc/traci.constants.html>)
        """
        return [
            constants.VAR_POSITION,
            # constants.VAR_ROUTE,
            constants.VAR_ROAD_ID,
            constants.VAR_SPEED,
        ]

    @staticmethod
    def from_simulation(
        simulation_object, updater: "SimulationObjectUpdatingComponent"
    ) -> None:
        # Nothing to do (we dont load trains from the sim)
        pass

    def add_simulation_connections(self) -> None:
        # Nothing to do (we dont load trains from the sim)
        pass
