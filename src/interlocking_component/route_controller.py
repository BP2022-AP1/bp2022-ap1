from abc import ABC, abstractmethod

import marshmallow as marsh
from peewee import BooleanField

from src.base_model import BaseModel


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

    def is_new_fahrstrasse_needed(self, train: "Train", track_segment: "Track"):
        """This method should be called when a train enters a new track_segment.
        It then checks if the train is near the end of his fahrstrasse and updates it, if necessary.

        :param train: the train that may need a new fahrstasse
        :type Train: Train
        :param track_segment: the track_segment it just entered
        :type Track: Track
        """
        raise NotImplementedError()

    def check_all_fahrstrassen_for_failures(self):
        """This method checks for all trains, if their fahrstrassen and routes are still valid."""
        raise NotImplementedError()
