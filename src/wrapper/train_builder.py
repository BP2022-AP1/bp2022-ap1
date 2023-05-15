from typing import List

from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Platform, Train


class TrainBuilder:
    """A factory to construct trains wich drive through the simulation"""

    def __init__(
        self,
        updater: SimulationObjectUpdatingComponent,
        route_controller: RouteController,
    ):
        self._updater: SimulationObjectUpdatingComponent = updater
        self.route_controller: RouteController = route_controller

    def spawn_train(
        self, identifier: str, timetable: List[str], train_type: str
    ) -> bool:
        """Spawns a new train in the simulation

        :param identifier: The id of the new train
        :param timetable: The stations the train drives along (as string-ids)
        :param train_type: the type of the train (corresponds to a sumo train type)
        :return: if the spawning was successful
        """
        timetable = self._convert_timetable(timetable)

        assert len(timetable) >= 2

        route = self._get_first_route(timetable[0], timetable[1])

        if not route:
            return False

        self._updater.simulation_objects.append(
            Train(identifier, timetable, train_type, self._updater)
        )

        return True

    def _get_first_route(self, from_platform: Platform, to_platform: Platform) -> str:
        return self.route_controller.set_spawn_fahrstrasse(
            from_platform.edge, to_platform.edge
        )

    def _convert_timetable(self, timetable: List[str]):
        converted = []
        timetable = [] if timetable is None else timetable
        for item in timetable:
            converted.append(
                next(x for x in self._updater.platforms if x.identifier == item)
            )

        return converted
