import os
from typing import List, Tuple

from interlocking.interlockinginterface import Interlocking
from interlocking.model.route import Route
from planpro_importer.reader import PlanProReader
from yaramo.signal import SignalDirection

from src.component import Component
from src.event_bus.event_bus import EventBus
from src.interlocking_component.infrastructure_provider import (
    SumoInfrastructureProvider,
)
from src.interlocking_component.router import Router
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge, Node, Platform, Track, Train


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
    routes_to_be_reserved: List[Route] = []
    tick: int = 0
    topology = None

    def __init__(
        self,
        event_bus: EventBus,
        priority: int,
        simulation_object_updating_component: SimulationObjectUpdatingComponent,
        path_name: str = os.path.join("data", "planpro", "schwarze_pumpe_v1.ppxml"),
    ):
        """This method instantiates the interlocking and the infrastructure_provider
        and must be called before the interlocking can be used.
        """
        super().__init__(event_bus, priority)
        self.simulation_object_updating_component = simulation_object_updating_component
        self.router = Router()

        # Import from local PlanPro file
        self.topology = PlanProReader(path_name).read_topology_from_plan_pro_file()

        infrastructure_provider = SumoInfrastructureProvider(self, event_bus)
        self.interlocking = Interlocking(infrastructure_provider)
        self.interlocking.prepare(self.topology)

    def initialize_signals(self):
        """This method sets which edge is the incoming for each signal."""
        print("Starting to initialize signals")
        for yaramo_signal in self.topology.signals.values():
            signal = None
            for potentical_signal in self.simulation_object_updating_component.signals:
                if yaramo_signal.name == potentical_signal.identifier:
                    signal = potentical_signal

            edges_into_signal = [
                edge for edge in signal.edges if edge.to_node == signal
            ]
            edges_numbers = [
                edge.identifier.split("-")[1] for edge in edges_into_signal
            ]

            if yaramo_signal.direction == SignalDirection.IN:
                if int(edges_numbers[0]) < int(edges_numbers[1]):
                    signal.incoming = edges_into_signal[0]
                else:
                    signal.incoming = edges_into_signal[1]
            else:
                if int(edges_numbers[0]) > int(edges_numbers[1]):
                    signal.incoming = edges_into_signal[0]
                else:
                    signal.incoming = edges_into_signal[1]
        print("Signals were initialized")

    def next_tick(self, tick: int):
        if tick == 1:
            self.initialize_signals()
        self.tick = tick
        for route, interlocking_route, train, route_length in self.routes_to_be_set:
            # This tries to set the fahrstrasse in the interlocking.
            # The Sumo route was already set and the route was reserved.
            was_set = self.try_setting_interlocking_route(
                route, interlocking_route, train, route_length
            )
            if was_set:
                self.routes_to_be_set.remove(
                    (route, interlocking_route, train, route_length)
                )

        for (
            route,
            train,
            interlocking_route,
            route_length,
        ) in self.routes_to_be_reserved:
            # This tries to reserve the route and then also set the interlocking route.
            # The Sumo route was set already.
            was_reserved = self.try_reserving_route(
                route, train, interlocking_route, route_length
            )
            if was_reserved:
                self.routes_to_be_reserved.remove(
                    (route, train, interlocking_route, route_length)
                )

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
        print("trying to set spawn fahrstraße")
        new_route = self.router.get_route(start_edge, end_edge)
        # new_route contains a list of signals from starting signal to end signal of the new route.

        for end_node_candidat in new_route[2:]:
            for interlocking_route in self.interlocking.routes:
                if (
                    interlocking_route.start_signal.yaramo_signal.name
                    == new_route[1].identifier
                    and interlocking_route.end_signal.yaramo_signal.name
                    == end_node_candidat.identifier
                ):
                    # This sets the route in the interlocking
                    was_set = self.interlocking.set_route(
                        interlocking_route.yaramo_route
                    )

                    print("set?", was_set)

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
        if train.station_index >= len(train.timetable):
            # if the train has reached the last station, don't allocate a new fahrstraße
            return

        routes = self._get_interlocking_routes_for_edge(edge)
        for route in routes:
            if route.get_last_segment_of_route() != edge.identifier.split("-re")[0]:
                continue

            self.set_fahrstrasse(train, edge)
            break

    def set_fahrstrasse(self, train: Train, edge: Edge):
        """This method can be called when a train reaches a platform,
        so that the route to the next platform can be set.

        :param train: the train
        :type train: Train
        :param edge: the edge it is currently on
        :type edge: Edge
        """
        new_route = self.router.get_route(
            edge, train.timetable[train.station_index].edge
        )
        # new_route contains a list of signals from starting signal to end signal of the new route.

        route_length = 0

        for i, end_node_candidat in enumerate(new_route[2:], start=2):
            route_length += new_route[i - 1].get_edge_to(end_node_candidat).length

            for interlocking_route in self.interlocking.routes:
                if (
                    interlocking_route.start_signal.yaramo_signal.name
                    == new_route[1].identifier
                    and interlocking_route.end_signal.yaramo_signal.name
                    == end_node_candidat.identifier
                ):
                    # This sets the route in SUMO.
                    # The SUMO route is also set when the interlocking fahrstrasse could not be set,
                    # so that the train waits in front of the next signal instead of disappearing.
                    # The Interlocking Route has the same id as the SUMO route.
                    train.route = interlocking_route.id

                    was_reserved = self.try_reserving_route(
                        new_route[:i], train, interlocking_route, route_length
                    )

                    if not was_reserved:
                        self.routes_to_be_reserved.append(
                            new_route[:i], train, interlocking_route, route_length
                        )
                    return
        # If the no interlocking route is found an error is raised
        raise KeyError()

    def try_reserving_route(
        self, route: List[Node], train, interlocking_route, route_length
    ) -> bool:
        """This method tries to reserve a route.

        :param route: the route to be reserved
        :param train: the train to reserve for
        :param interlocking_route: the corresponding interlocking route
        :param route_length: the length of the route
        :return: if it was successful
        """
        was_reserved = self.reserve_route(route, train)

        was_set = self.try_setting_interlocking_route(
            route, interlocking_route, train, route_length
        )
        if not was_set:
            self.routes_to_be_set.append(
                (route, interlocking_route, train, route_length)
            )
        return was_reserved

    def try_setting_interlocking_route(
        self, route: List[Node], interlocking_route, train: Train, route_length: int
    ) -> bool:
        """This method tries to set the interlocking route.

        :param route: the route to set
        :param interlocking_route: the corresponding interlocking route
        :param train: the train to set the route for (needed for logging)
        :param route_length: the length of the route (nedded for logging)
        :return: if it was successful
        """
        if not self.check_if_route_is_reserved(route, train):
            return False

        # This sets the route in the interlocking
        was_set = self.interlocking.set_route(interlocking_route.yaramo_route)
        if was_set:
            self.event_bus.create_fahrstrasse(self.tick, interlocking_route.id)
            self.event_bus.train_enter_block_section(
                self.tick,
                train.identifier,
                interlocking_route.id,
                route_length,
            )
            # Right now a fahrstrasse is always from one Signal to the next.
            # Because of this the fahrstrasse is identical
            # to the block section the train drives into.
        return was_set

    def check_if_route_is_reserved(self, route: List[Node], train) -> bool:
        """This method checks, if the given route is fully reserved for the given train
        and if the train is in the first position in the queue.

        :param route: the route to check
        :param train: the train to check for
        :return: if the route is reserved for the train
        """
        route_as_tracks = self.get_tracks_of_node_route(route)
        for track in route_as_tracks:
            if track.reservations[0][0] != train:
                return False
        return True

    def reserve_route(self, route: List[Node], train: Train) -> bool:
        """This method reserves a route and returns, if it was successful.

        :param route: the route to reserve
        :param train: the train the route should be reserved for
        :return: if it was successful
        """
        route_as_edges = self.get_edges_of_node_route(route)
        recursiv_reservation_worked = True
        tracks_to_be_reserved: List[Tuple[Train, Track]] = []

        train_reservation_start = len(train.reserved_tracks)

        if self.check_if_reservation_ends_in_opposing_reservation(route):
            return False

        for edge in route_as_edges:
            track = edge.track
            if len(track.reservations) != 0:
                reserving_train = track.reservations[-1][0]
                last_track_of_reserving_train = reserving_train.reserved_tracks[-1]
                if last_track_of_reserving_train == track:
                    if reserving_train.station_index != len(reserving_train.timetable):
                        # When the reservation reached the end of the trains route,
                        # there will be no more reservations.
                        route = self.router.get_route(
                            track,
                            reserving_train.timetable[reserving_train.station_index],
                        )
                        was_reserved = self.reserve_route(route, reserving_train)
                        if not was_reserved:
                            recursiv_reservation_worked = False
            tracks_to_be_reserved.append((train, track, edge))
        if recursiv_reservation_worked is False:
            return False
        for i, (train_to_be_reserved, track, edge) in enumerate(tracks_to_be_reserved):
            track.reservations.append((train_to_be_reserved, edge))
            train_to_be_reserved.reserved_tracks.insert(
                train_reservation_start + i, track
            )
        return True

    def check_if_reservation_ends_in_opposing_reservation(
        self, route: List[Node]
    ) -> bool:
        """This method checks if the given route ends on a track,
        that is reserved for a train in the opposing direction.

        :param route: the route to check
        :return: if  the last track is reserved for a train in the opposing direction
        """
        route_as_edges = self.get_edges_of_node_route(route)
        last_edge = route_as_edges[-1]
        # If a route to be reserved leads into a track that is reserved for
        # or occupied by an opposing train, i.e. a train that will leave that
        # section by moving into the section the route to be reserved comes from,
        # the reservation of that route fails.
        for _, edge in last_edge.track.reservations:
            if edge != last_edge:
                return False
        return True

    def get_tracks_of_node_route(self, route: List[Node]) -> List[Track]:
        """This method returns a list of tracks corresponding to the given list of nodes.

        :param route: the route as nodes
        :return: the route as tracks
        """
        track_route = []
        for i in range(len(route[:-1])):
            track = route[i].get_edge_to(route[i + 1]).track
            track_route.append(track)
        return track_route

    def get_edges_of_node_route(self, route: List[Node]) -> List[Edge]:
        """This method returns a list of edges corresponding to the given list of nodes.

        :param route: the route as nodes
        :return: the route as edges
        """
        edge_route = []
        for i in range(len(route[:-1])):
            edge = route[i].get_edge_to(route[i + 1])
            edge_route.append(edge)
        return edge_route

    def maybe_free_fahrstrasse(self, train: Train, edge: Edge):
        """This method checks if the given edge is the last segment of a activ route
        and frees it if so.

        :param train: The train that drove of an edge
        :type train: Train
        :param edge: The edge the train drove off of
        :type edge: Edge
        """
        routes = self._get_interlocking_routes_for_edge(edge)
        for route in routes:
            if route.get_last_segment_of_route() != edge.identifier.split("-re")[0]:
                continue

            self._free_fahrstrasse(train, route)

    def _free_fahrstrasse(self, train: Train, route: Route):
        """This method frees the given interlocking route.

        :param train: The train that drove of an edge
        :type train: Train
        :param route: The active route
        :type route: Route
        """
        if route is not None:
            # This frees the route in the interlocking
            self.interlocking.free_route(route.yaramo_route)
            self.event_bus.remove_fahrstrasse(self.tick, route.id)
            self.event_bus.train_leave_block_section(
                self.tick, train.identifier, route.id, 0
            )

    def _get_interlocking_routes_for_edge(self, edge: Edge) -> List[Route]:
        """This method returns the interlocking route corresponding to the given edge.

        :param edge: The edge to which the route is searched
        :type edge: Edge
        :return: The interlocking Route corresponding to the edge
        :rtype: Route
        """
        routes = []
        for route_candidate in self.interlocking.active_routes:
            interlocking_track_candidat = route_candidate.contains_segment(
                edge.identifier.split("-re")[0]
            )
            # The -re part of the identifier must be cut,
            # because the interlocking does not know of reverse directions.
            # A track can be part of many routes, but only ever part of one active route.

            if interlocking_track_candidat is not None:
                routes.append(route_candidate)
        return routes

    def check_all_fahrstrassen_for_failures(self):
        """This method checks for all trains, if their fahrstrassen and routes are still valid."""
        raise NotImplementedError()
