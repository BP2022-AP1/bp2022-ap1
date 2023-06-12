from typing import List, Tuple

import traci

from src.interlocking_component.route_controller import (
    RouteController,
    UninitializedTrain,
)
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Train


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
        timetable: List[Platform] = self._convert_timetable(timetable)

        assert len(timetable) >= 2

        starting_edge = timetable[0].edge.from_node.get_edges_accessible_from(
            timetable[0].edge
        )[0]

        route, reservation_placeholder = self._get_first_route(timetable, starting_edge)

        if not route:
            return False

        train = Train(identifier, timetable, train_type, self._updater, route_id=route)
        traci.vehicle.subscribe(train.identifier, train.add_subscriptions())

        self._updater.simulation_objects.append(train)

        self.route_controller.reserve_for_initialized_train(
            reservation_placeholder, train
        )

        return True

    def _get_first_route(
        self, timetable: List[Platform], starting_edge: Edge
    ) -> Tuple[str, UninitializedTrain]:
        return self.route_controller.set_spawn_fahrstrasse(timetable, starting_edge)

    def _convert_timetable(self, timetable: List[str]):
        converted = []
        timetable = [] if timetable is None else timetable
        for item in timetable:
            converted.append(
                next(x for x in self._updater.platforms if x.identifier == item)
            )

        return converted
