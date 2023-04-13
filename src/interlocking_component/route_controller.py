from abc import ABC, abstractmethod

import marshmallow as marsh
from interlocking import interlockinginterface
from peewee import BooleanField

from src.base_model import BaseModel
from src.interlocking_component.router import Router
from src.wrapper.simulation_objects import Track, Train


class InterlockingConfiguration(BaseModel):
    """This class contains all fields needed to configure the Interlocking and RouteController"""

    class Schema(BaseModel.Schema):
        """Schema for the InterlockingConfiguration"""

        dynamicRouting = marsh.fields.Boolean()

        def _make(self, data: dict) -> "InterlockingConfiguration":
            return InterlockingConfiguration(**data)

    dynamicRouting = BooleanField(default=False)


class IRouteController(ABC):
    """An abstract Interface to call funtions on the RouteController."""

    @abstractmethod
    def set_spawn_route(self, platforms: list("Plattform")) -> str:
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

    def insert_track_blocked(self, track: "Track"):
        """This method is used to block a track and recalculate the routes of relevant trains.

        :param track_id: the id of the blocked track
        :type track_id: str
        """
        raise NotImplementedError()

    def insert_track_unblocked(self, track: "Track"):
        """This method is used to unblock a track and recalculate the routes of relevant trains.

        :param track_id: the id of the unblocked track
        :type track_id: str
        """
        raise NotImplementedError()

    def insert_platform_blocked(self, platform: "Platform"):
        """This method is used to block a platform and recalculate the routes
        and stops of relevant trains.

        :param platform_id: the id of the blocked platform
        :type platform_id: str
        """
        raise NotImplementedError()

    def insert_platform_unblocked(self, platform: "Platform"):
        """This method is used to unblock a platform and recalculate the routes
        and stops of relevant trains.

        :param platform_id: the id of the unblocked platform
        :type platform_id: str
        """
        raise NotImplementedError()

    def insert_track_speed_limit_changed(self, track: "Track"):
        """This method is used to notify the interlocking about a changed track speed limit,
        so that it can recalculate the routing of relevant trains.

        :param track_id: the id of the track, which speedlimit changed
        :type track_id: str
        """
        raise NotImplementedError()

    def insert_train_max_speed_changed(self, train: "Train"):
        """This method is used to notify the interlocking about a changed train speed limit,
        so that it can recalculate the routing of relevant trains.

        :param train_id: the id of the train, which speed limit changed
        :type train_id: str
        """
        raise NotImplementedError()


class RouteController(IRouteController):
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    interlocking: interlockinginterface = None
    router: Router = None

    def is_new_fahrstrasse_is_needed(self, train: Train, track: Track) -> bool:
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
                track.identifier
            )
            # This assumes, that track.identifier does not contain '-re',
            # as the interlocking does not know of reverse directions.
            if interlocking_track_candidat is not None:
                route = route_candidate
        if route is None or route.get_last_segment_of_route != track.identifier:
            return false

        new_route = self.router.get_route(track, train.timetable[0].track)
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
                    return True
        return False

    def check_all_fahrstrassen_for_failures(self):
        """This method checks for all trains, if their fahrstrassen and routes are still valid."""
        raise NotImplementedError()
