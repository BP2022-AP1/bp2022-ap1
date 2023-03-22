#!/usr/bin/env python3

from threading import Thread
from typing import List

import traci
from sumolib import checkBinary

from src.component import Component
from src.wrapper.simulation_component import SimulationComponent


class Communicator(Thread):
    """Component used for communicating with a sumo simulation using traci."""

    _configuration = None
    _port = None
    _components = None
    _current_tick = 1
    _max_tick = None

    _stopped = False

    @property
    def progress(self):
        """Get the current simulation progress as a float between 0 and 1

        :return: The current simulation progress
        :rtype: float
        """
        return self._current_tick / self._max_tick

    def __init__(
        self,
        components: List[Component] = None,
        max_tick: int = 86_400,
        sumo_port: int = None,
        sumo_configuration: str = "sumo-config/example.scenario.sumocfg",
    ):
        """Creates a new Communicator object"""
        Thread.__init__(self)
        self._configuration = sumo_configuration
        self._port = sumo_port
        self._components = components if components is not None else []
        self._max_tick = max_tick

    def run(self):
        """Starts sumo (no gui) and connects using traci. The connection has the `default` label."""

        traci.start([checkBinary("sumo"), "-c", self._configuration], port=self._port)

        while not self._stopped and self._current_tick <= self._max_tick:
            for component in self._components:
                component.next_tick(self._current_tick)
            self._simulation_step()
            self._current_tick += 1

        traci.close(wait=False)

    def stop(self):
        """Stopps the simulation requesting a simulation step.
        At most, one simulation step will happen after this request"""
        self._stopped = True

    def _simulation_step(self):
        """Advances the simulation by one step"""
        traci.simulationStep()
