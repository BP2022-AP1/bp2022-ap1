from abc import ABC, abstractmethod

from interlocking import interlockinginterface

from src.interlocking_component.router import Router
from src.wrapper.simulation_objects import Platform, Track, Train


class IRouteController(ABC):
    """An abstract Interface to call funtions on the RouteController."""

    @abstractmethod
    def set_spawn_route(self, start_track: Track, end_track: Track) -> str:
        """This method can be called when instanciating a train
        to get back the first SUMO Route it should drive.
        This also sets a fahrstrasse for that train.

        :param platforms: A List of the Platforms the train will drive to.
        :type platforms: list
        :return: The id of the first SUMO Route.
        :rtype: str
        """
        raise NotImplementedError()

    @abstractmethod
    def start_interlocking(self):
        """This method sets up the interlocking"""
        raise NotImplementedError()


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


class RouteController(IRouteController):
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    interlocking: interlockinginterface = None
    router: Router = None

    def set_spawn_route(self, start_track: Track, end_track: Track) -> str:
        """This method can be called when instanciating a train
        to get back the first SUMO Route it should drive.
        This also sets a fahrstrasse for that train.

        :param start_track: The track from where the route should start
        :type start_track: Track
        :param end_track: The track where the route should end
        :type end_track: Track
        :raises KeyError: _description_
        :return: The id of the first SUMO Route.
        :rtype: str
        """
        new_route = self.router.get_route(start_track, end_track)
        # new_route contains a list of signals from starting signal to end signal of the new route.

        for end_node_candidat in new_route:
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

    def maybe_update_fahrstrasse(self, train: Train, track: Track):
        """This method should be called when a train enters a new track_segment.
        It then checks if the train is near the end of his fahrstrasse and updates it, if necessary.

        :param train: the train that may need a new fahrstasse
        :type Train: Train
        :param track_segment: the track it just entered
        :type Track: Track
        """
        route = None
        for route_candidate in self.interlocking.active_routes:
            interlocking_track_candidat = route_candidate.contains_segment(
                track.identifier.split("-re")[0]
            )
            # The -re part of the identifier must be cut,
            # because the interlocking does not know of reverse directions.

            if interlocking_track_candidat is not None:
                route = route_candidate
        if route is None or route.get_last_segment_of_route != track.identifier:
            return

        new_route = self.router.get_route(track, train.timetable[0].track)
        # new_route contains a list of signals from starting signal to end signal of the new route.

        for end_node_candidat in new_route:
            for interlocking_route in self.interlocking.routes:
                if (
                    interlocking_route.start_signal.name == new_route[0]
                    and interlocking_route.end_signal.name == end_node_candidat
                ):
                    # This sets the route in the interlocking
                    self.interlocking.set_route(interlocking_route.yaramo_route)
                    # This does not check if the route can even be set and does not handle,
                    # if it can not be set this simulation step.

                    # This frees the least route in the interlocking
                    self.interlocking.free_route(route.yaramo_route)
                    # This may not be the best place (time) to do so,
                    # as the route schould be freed when the train leaves the route
                    # and not when it is still on the last segment.

                    # This sets the route in SUMO.
                    # The Interlocking Route has the same id as the SUMO route.
                    train.route = interlocking_route.id
                    return

    def check_all_fahrstrassen_for_failures(self):
        """This method checks for all trains, if their fahrstrassen and routes are still valid."""
        raise NotImplementedError()
