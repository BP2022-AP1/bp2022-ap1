#!/usr/bin/env python3

from sumolib import checkBinary
import traci


class Communicator:
    """Component used for communicating with a sumo simulation using traci.
    The global traci object is exposed via the connection property"""

    connection = None
    _configuration = None
    _port = None

    def __init__(self, sumo_port: int = None, configuration: str = "test.sumocfg"):
        """Creates a new Communicator object"""
        self._configuration = configuration
        self._port = sumo_port

    def start(self):
        """Starts sumo (no gui) and connects using traci. The connection has the `default` label."""
        traci.start([checkBinary("sumo"), "-c", self._configuration], port=self._port)
        self.connection = traci

    def stop(self):
        """Stopps the simulation by immediatly closing the traci connection"""
        traci.close(wait=False)

    def simulation_step(self):
        """Advances the simulation by one step"""
        traci.simulationStep()
