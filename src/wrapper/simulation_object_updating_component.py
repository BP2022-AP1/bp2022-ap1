from os import path
from typing import List

import sumolib
import traci

from src.component import Component
from src.logger.logger import Logger
from src.wrapper.simulation_objects import (
    Edge,
    Node,
    Platform,
    Signal,
    SimulationObject,
    Switch,
    Track,
    Train,
)


class SimulationObjectUpdatingComponent(Component):
    """Keeps all simulation objects updated by updating them with
    their subscription results from the current tick.
    Also handles the adding and removing of objects from the simulation.
    """

    _simulation_objects = None
    _sumo_configuration = None

    @property
    def simulation_objects(self) -> List[SimulationObject]:
        """Returns a list of all objects in the simulation

        :return: the objects in the simulation
        """
        return self._simulation_objects

    @property
    def trains(self) -> List[Train]:
        """Returns all trains in the simulation

        :return: The trains in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Train)]

    @property
    def nodes(self) -> List[Node]:
        """Returns all nodes in the simulation

        :return: The nodes in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Node)]

    @property
    def switches(self) -> List[Switch]:
        """Returns all switches in the simulation

        :return: The switches in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Switch)]

    @property
    def signals(self) -> List[Signal]:
        """Returns all signals in the simulation

        :return: The signals in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Signal)]

    @property
    def platforms(self) -> List[Platform]:
        """Returns all platforms in the simulation

        :return: The platforms in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Platform)]

    @property
    def edges(self) -> List[Edge]:
        """Returns all tracks in the simulation

        :return: The tracks in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Edge)]

    @property
    def tracks(self) -> List[Track]:
        """Returns all tracks in the simulation

        :return: The tracks in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Track)]

    def __init__(
        self,
        logger: Logger = None,
        sumo_configuration: str = None,
    ):
        """Creates a new SimulationObjectUpdatingComponent.

        :param logger: The logger to send events to, defaults to None
        :param sumo_configuration: the path to the `.sumocfg` file
        (relative to the root of the project), defaults to None
        """
        super().__init__(priority=10, logger=logger)
        self._simulation_objects = []
        self._sumo_configuration = sumo_configuration
        if sumo_configuration is not None:
            self._fetch_initial_simulation_objects()

    def next_tick(self, tick: int):
        subscription_results = traci.simulation.getAllSubscriptionResults()

        for simulation_object in self._simulation_objects:
            simulation_object.update(subscription_results[simulation_object.traci_id])

        self._remove_stale_vehicles()

    def _remove_stale_vehicles(self):
        simulation_vehicles = set(traci.vehicle.getIDList())
        stored_vehicles = set((train.identifier for train in self.trains))

        vehicles_to_remove = stored_vehicles - simulation_vehicles

        for vehicle in vehicles_to_remove:
            self._simulation_objects.remove(
                next(train for train in self.trains if train.identifier == vehicle)
            )

    def _fetch_initial_simulation_objects(self):
        folder = path.dirname(self._sumo_configuration)
        inputs = next(sumolib.xml.parse(self._sumo_configuration, "input"))
        net_file = path.join(folder, inputs["net-file"][0].getAttribute("value"))
        additional_file = path.join(
            folder, inputs["additional-files"][0].getAttribute("value")
        )
        net = sumolib.net.readNet(net_file)
        platforms = list(sumolib.xml.parse(additional_file, "busStop")) + list(
            sumolib.xml.parse(additional_file, "trainStop")
        )

        # signals
        self._simulation_objects += [
            Signal.from_simulation(signal, self) for signal in net.getTrafficLights()
        ]

        # switches
        self._simulation_objects += [
            Switch.from_simulation(node, self)
            for node in net.getNodes()
            if len(node.getConnections()) >= 3
        ]

        # other nodes
        self._simulation_objects += list(
            filter(
                lambda x: x is not None,
                (
                    Node.from_simulation(node, self)
                    for node in net.getNodes()
                    if len(node.getConnections()) < 3
                ),
            )
        )

        # Edges
        self._simulation_objects += [
            Edge.from_simulation(edge, self) for edge in net.getEdges()
        ]

        # Tracks
        for edge in (x for x in self.edges if x.track is None):
            if edge.identifier.endswith("-re"):
                identifier = edge.identifier.split("-re")[0]
            else:
                identifier = edge.identifier + "-re"

            reverse = [x for x in self.edges if x.identifier == identifier][0]
            self._simulation_objects.append(Track(edge, reverse))

        # platforms
        self._simulation_objects += [
            Platform.from_simulation(platform, self) for platform in platforms
        ]

        for simulation_object in self._simulation_objects:
            simulation_object.add_simulation_connections()
