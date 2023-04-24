from typing import List

from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Platform, Train


class TrainSpawner:
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
        timetable = self._convert_timetable(timetable)

        route = self._get_first_route()

        if route is None:
            return False

        Train(identifier, timetable, train_type, self._updater)

        return True

    def _get_first_route(self, from_platform: Platform, to_platform: Platform) -> str:
        return self.route_controller.set_spawn_route(
            from_platform.track, to_platform.track
        )

    def _convert_timetable(self, timetable: List[str]):
        converted = []
        timetable = [] if timetable is None else timetable
        for item in timetable:
            converted.append(
                next(x for x in self.updater.platforms if x.identifier == item)
            )

        return converted
