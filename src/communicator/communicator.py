#!/usr/bin/env python3
import os
import pickle
from typing import Callable, List
from uuid import UUID

import traci
from celery import Task
from celery.result import AsyncResult
from sumolib import checkBinary

from src.communicator.celery import celery
from src.component import Component


class Communicator:
    """Component used for communicating with a sumo simulation using traci."""

    _configuration = None
    _port = None
    _components = None
    _max_tick = None

    def add_component(self, component: Component):
        """Add the given component to the simulation.
        There are no guarantees if the component will be called within
        the current simualtion tick.

        :param component: The component to add to the current simulation
        """
        self._components.append(component)

    def __init__(
        self,
        components: List[Component] = None,
        max_tick: int = 86_400,
        sumo_port: int = None,
        sumo_configuration: str = os.path.join(
            "data", "sumo", "schwarze_pumpe_v1", "sumo-config", "schwarze_pumpe_v1.scenario.sumocfg"
        ),
    ):
        """Creates a new Communicator object"""
        self._configuration = sumo_configuration
        self._port = sumo_port
        self._components = components if components is not None else []
        self._max_tick = max_tick

    def run(self) -> str:
        """
        This function starts the simulation and returns the id of the celery task.
        Therefore it collects and serializes the configuration and starts a new celery process.
        The id can be used to stop the simulation or to get the current progress.

        :return: The id of the celery task
        """
        celery_disabled = os.getenv("DISABLE_CELERY", False)

        if not celery_disabled:
            process = self._run.delay(
                max_tick=self._max_tick,
                components_pickle=pickle.dumps(self._components),
                configuration=self._configuration,
                port=self._port,
            )
            return process.id
        else:
            self._run_with_gui()
            return "no id available"

    def _run_with_gui(self):
        delay = os.getenv("SUMO_GUI_DELAY", 10)
        traci.start(
            [
                checkBinary("sumo-gui"),
                "-c",
                self._configuration,
                "--start",
                "--quit-on-end",
                "--delay",
                delay,
            ],
            port=self._port,
        )

        run_simulation_steps(self._components, self._max_tick)

        traci.close(wait=False)

    @celery.task(bind=True, ignore_result=False)
    def _run(
        self: Task,
        max_tick: int,
        components_pickle: bytes,
        configuration: str,
        port: int,
    ):
        """
        Starts sumo (no gui) and connects using traci.
        This function is called by celery and should not be called directly.
        It runs inside a celery process and therefore can be stopped using the celery task id.

        :param max_tick: The maximum number of ticks to simulate
        :param components_pickle: The serialized components
        :param configuration: The sumo configuration file location
        :param port: The port to use for the sumo simulation
        """

        components = pickle.loads(components_pickle)
        traci.start([checkBinary("sumo"), "-c", configuration], port=port)

        def update_state(max_tick: int, current_tick: int, sumo_running: bool):
            self.update_state(
                state="PROGRESS",
                meta={
                    "sumo_running": sumo_running,
                    "current": current_tick,
                    "total": max_tick,
                },
            )

        run_simulation_steps(components, max_tick, update_state)

        traci.close(wait=False)

    @classmethod
    def stop(cls, process_id: str):
        """
        Stopps the celery process.

        :param process_id: The id of the celery task
        """
        process = AsyncResult(process_id)
        process.revoke()

    @classmethod
    def progress(cls, process_id: str) -> float:
        """Get the current simulation progress as a float between 0 and 1

        :return: The current simulation progress
        :rtype: float
        """
        process = AsyncResult(str(process_id))
        return process.info.get("current") / process.info.get("total")

    @classmethod
    def state(cls, progress_id: str) -> str:
        """
        Get the current state of the simulation.
        Possible states are: PENDING, STARTED, RETRY, FAILURE, SUCCESS.

        :param progress_id: The id of the celery task
        :return: The current state of the simulation
        """
        process = AsyncResult(progress_id)
        return process.status


def dummy_update_state(current_tick: int, max_tick: int, sumo_running: bool):
    return None


def run_simulation_steps(
    components: list[Component],
    max_tick: int,
    update_state: Callable[[int, int, bool], None] = dummy_update_state,
):
    """
    Function to run the simulation steps.
    This function requires traci and sumo to be started and connected.

    :param components: The components to run
    :param max_tick: The maximum number of ticks to simulate
    :param update_state: A function to update the state of the simulation
    """
    sumo_running = True
    current_tick = 1

    update_state(current_tick, max_tick, sumo_running)

    while current_tick <= max_tick:
        for component in components:
            component.next_tick(current_tick)
        traci.simulationStep()
        current_tick += 1
        update_state(current_tick, max_tick, sumo_running)

    sumo_running = False
    update_state(current_tick, max_tick, sumo_running)
