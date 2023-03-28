from typing import List, Protocol


class ISimulationObjectsUpdater(Protocol):
    """Updates and stores references to the python simulation objects"""

    objects: List[ISimulationObject]
    trains: List[ISimulationTrain]
    signals: List[ISimulationSignal]
    switches: List[ISimulationSwitch]
    edges: List[ISimulationEdge]
    platforms: List[ISimulationPlatform]

    def next_tick(self, tick: int) -> None:
        """Updates the simulation objects with the new state from SUMO.

        :param tick: The current simulation tick
        """
