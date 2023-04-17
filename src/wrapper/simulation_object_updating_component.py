from typing import List

import sumolib
import traci

from src.component import Component
from src.wrapper.simulation_objects import (
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
    def tracks(self) -> List[Track]:
        """Returns all tracks in the simulation

        :return: The tracks in the simulation
        """
        return [x for x in self._simulation_objects if isinstance(x, Track)]

    def __init__(
        self,
        logger=None,
        sumo_configuration=None,
    ):
        super().__init__(priority=10, logger=logger)
        self._simulation_objects = []
        self._sumo_configuration = sumo_configuration
        if sumo_configuration is not None:
            self._fetch_initial_simulation_objects()

    def next_tick(self, tick: int):
        subscription_results = traci.simulation.getAllSubscriptionResults()

        for simulation_object in self._simulation_objects:
            simulation_object.update(subscription_results[simulation_object.traci_id])

    def _fetch_initial_simulation_objects(self):
        net_file = next(
            sumolib.xml.parse(self._sumo_configuration, "net-file")
        ).getAttribute("value")
        net = sumolib.net.readNet(net_file)

        # Tracks
        self._simulation_objects += [
            Track.from_simulation(edge, self) for edge in net.getEdges()
        ]

        # self._simulation_objects += [
        #    Node.from_simulation(node, self)
        #    for node in net.getNodes()
        #    if len(node.getConnections()) < 3
        # ]

        self._simulation_objects += [
            Switch.from_simulation(node, self)
            for node in net.getNodes()
            if len(node.getConnections()) >= 3
        ]

        # signals
        self._simulation_objects += [
            Signal.from_simulation(signal, self) for signal in net.getTrafficLights()
        ]

        # platforms
