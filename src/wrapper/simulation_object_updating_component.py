from typing import List

import traci

import src.wrapper.simulation_objects
from src.component import Component


class SimulationObjectUpdatingComponent(Component):
    """Keeps all simulation objects updated by updating them with
    their subscription results from the current tick.
    Also handles the adding and removing of objects from the simulation.
    """

    _simulation_objects = None

    @property
    def platforms(self) -> List["Platform"]:
        """Returns all platforms in the simulation

        :return: The platforms in the simulation
        """
        return [
            x
            for x in self._simulation_objects
            if isinstance(x, src.wrapper.simulation_objects.Platform)
        ]

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self._simulation_objects = []

        self._fetch_initial_simulation_objects()

    def next_tick(self, tick: int):
        subscription_results = traci.simulation.getAllSubscriptionResults()

        for simulation_object in self._simulation_objects:
            simulation_object.update(subscription_results[simulation_object.traci_id])

    def _fetch_initial_simulation_objects(self):
        pass
