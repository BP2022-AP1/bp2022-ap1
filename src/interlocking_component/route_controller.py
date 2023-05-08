import os
from typing import List

from interlocking.interlockinginterface import Interlocking
from interlocking.model.route import Route
from planpro_importer.reader import PlanProReader
from railwayroutegenerator.routegenerator import RouteGenerator

from src.component import Component
from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.router import Router
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Platform, Track, Train, Node


class IInterlockingDisruptor:
    """This class is the Interface to inject faults into the interlocking
    as well as to notify the Interlocking faults that occur in other parts of the simulation.
    """

    def insert_track_blocked(self, track: Track):
        """This method is used to block a track and recalculate the routes of relevant trains.

        :param track: the blocked track
        :type track: Track
        """
        raise NotImplementedError()

    def insert_track_unblocked(self, track: Track):
        """This method is used to unblock a track and recalculate the routes of relevant trains.

        :param track: the unblocked track
        :type track: Track
        """
        raise NotImplementedError()

    def insert_platform_blocked(self, platform: Platform):
        """This method is used to block a platform and recalculate the routes
        and stops of relevant trains.

        :param platform: the blocked platform
        :type platform: Platform
        """
        raise NotImplementedError()

    def insert_platform_unblocked(self, platform: Platform):
        """This method is used to unblock a platform and recalculate the routes
        and stops of relevant trains.

        :param platform: the unblocked platform
        :type platform: Platform
        """
        raise NotImplementedError()

    def insert_track_speed_limit_changed(self, track: Track):
        """This method is used to notify the interlocking about a changed track speed limit,
        so that it can recalculate the routing of relevant trains.

        :param track: the track, which speedlimit changed
        :type track: Track
        """
        raise NotImplementedError()

    def insert_train_max_speed_changed(self, train: Train):
        """This method is used to notify the interlocking about a changed train speed limit,
        so that it can recalculate the routing of relevant trains.

        :param train: the train, which speed limit changed
        :type train: Train
        """
        raise NotImplementedError()

    def insert_train_priority_changed(self, train: Train):
        """This method is used to notify the interlocking about a changed train priority,
        so that it can recalculate the routing of relevant trains.

        :param train: the train, which priority changed
        :type train: Train
        """
        raise NotImplementedError()


class RouteController(Component):
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    interlocking: Interlocking = None
    router: Router = None
    simulation_object_updating_component: SimulationObjectUpdatingComponent = None
    routes_to_be_set: List[Route] = []
    tick: int = None

    def __init__(
        self,
        logger: Logger,
        priority: int,
        simulation_object_updating_component: SimulationObjectUpdatingComponent,
        path_name: str = os.path.join("data", "planpro", "test_example.ppxml"),
    ):
        """This method instantiates the interlocking and the infrastructure_provider
        and must be called before the interlocking can be used.
        """
        super().__init__(logger, priority)
        self.simulation_object_updating_component = simulation_object_updating_component
        self.router = Router()

        # Import from local PlanPro file
        topology = PlanProReader(path_name).read_topology_from_plan_pro_file()

        # Generate Routes
        # I'm not sure if this is necessary, but better save than sorry.
        RouteGenerator(topology).generate_routes()

        infrastructure_provider = SumoInfrastructureProvider(self)
        self.interlocking = Interlocking(infrastructure_provider)
        self.interlocking.prepare(topology)

    def next_tick(self, tick: int):
        self.tick = tick
        for interlocking_route in self.routes_to_be_set:
            # This sets the fahrstrasse in the interlocking.
            # The Sumo SUMO route was already set.

            was_set = self.interlocking.set_route(interlocking_route.yaramo_route)

            if was_set:
                self.routes_to_be_set.remove(interlocking_route)

    def set_spawn_fahrstrasse(self, start_edge: Edge, end_edge: Edge) -> str:
        """This method can be called when instanciating a train
        to get back the first SUMO Route it should drive.
        This also sets a fahrstrasse for that train.

        :param start_edge: The edge from where the route should start
        :type start_edge: Edge
        :param end_edge: The edge where the route should end
        :type end_edge: Edge
        :raises KeyError: The route could not be found in the interlocking.
        :return: The id of the first SUMO Route.
        :rtype: str
        """
        new_route = self.router.get_route(start_edge, end_edge)
        # new_route contains a list of signals from starting signal to end signal of the new route.

        for end_node_candidat in new_route[1:]:
            for interlocking_route in self.interlocking.routes:
                if (
                    interlocking_route.start_signal.name == new_route[0]
                    and interlocking_route.end_signal.name == end_node_candidat
                ):
                    # This sets the route in the interlocking
                    was_set = self.interlocking.set_route(
                        interlocking_route.yaramo_route
                    )

                    if was_set:
                        # The Interlocking Route has the same id as the SUMO route.
                        # So this is also the id of the SUMO route.
                        return interlocking_route.id
                    # If the route can not be set in the interlocking None is returned,
                    # so that the spawner can try again next tick.
                    return None
        # If the no interlocking route is found an error is raised
        raise KeyError()

    def maybe_set_fahrstrasse(self, train: Train, edge: Edge):
        """This method should be called when a train enters a new track_segment.
        It then checks if the train is near the end of his fahrstrasse and updates it, if necessary.

        :param train: the train that may need a new fahrstasse
        :type train: Train
        :param edge: the edge it just entered
        :type edge: Edge
        """
        route = self._get_interlocking_route_for_edge(edge)
        if route is None or route.get_last_segment_of_route != edge.identifier:
            return

        self.set_fahrstrasse(train, edge)

    def set_fahrstrasse(self, train: Train, edge: Edge):
        """This method can be called when a train reaches a platform,
        so that the route to the next platform can be set.

        :param train: the train
        :type train: Train
        :param edge: the edge it is currently on
        :type edge: Edge
        """
        new_route = self.router.get_route(edge, train.timetable[0].edge)
        # new_route contains a list of signals from starting signal to end signal of the new route.

        for end_node_candidat in new_route[1:]:
            for interlocking_route in self.interlocking.routes:
                if (
                    interlocking_route.start_signal.name == new_route[0]
                    and interlocking_route.end_signal.name == end_node_candidat
                ):
                    # This sets the route in the interlocking
                    was_set = self.interlocking.set_route(
                        interlocking_route.yaramo_route
                    )
                    if was_set:
                        self.logger.create_fahrstrasse(self.tick, interlocking_route.id)
                    else:
                        self.routes_to_be_set.append(interlocking_route)

                    # This sets the route in SUMO.
                    # The SUMO route is also set when the interlocking fahrstrasse could not be set,
                    # so that the train waits in front of the next signal instead of disappearing.
                    # The Interlocking Route has the same id as the SUMO route.
                    train.route = interlocking_route.id
                    return

    def maybe_free_fahrstrasse(self, edge: Edge):
        """This method checks if the given edge is the last segment of a activ route
        and frees it if so.

        :param edge: the edge the train drove off of
        :type edge: Edge
        """
        route = self._get_interlocking_route_for_edge(edge)
        if route is None or route.get_last_segment_of_route != edge.identifier:
            return

        self._free_fahrstrasse(route)

    def _free_fahrstrasse(self, route: Route):
        """This method frees the given interlocking route.

        :param route: The active route
        :type route: Route
        """
        if route is not None:
            # This frees the route in the interlocking
            self.interlocking.free_route(route.yaramo_route)
            self.logger.remove_fahrstrasse(self.tick, route.id)

    def _get_interlocking_route_for_edge(self, edge: Edge) -> Route:
        """This method returns the interlocking route corresponding to the given edge.

        :param edge: The edge to which the route is searched
        :type edge: Edge
        :return: The interlocking Route corresponding to the edge
        :rtype: Route
        """
        for route_candidate in self.interlocking.active_routes:
            interlocking_track_candidat = route_candidate.contains_segment(
                edge.identifier.split("-re")[0]
            )
            # The -re part of the identifier must be cut,
            # because the interlocking does not know of reverse directions.
            # A track can be part of many routes, but only ever part of one active route.

            if interlocking_track_candidat is not None:
                return route_candidate
        return None

    def check_all_fahrstrassen_for_failures(self):
        """This method checks for all trains, if their fahrstrassen and routes are still valid."""
        raise NotImplementedError()
