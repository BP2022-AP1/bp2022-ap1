import marshmallow as marsh
from peewee import BooleanField

from src.base_model import BaseModel
from src.component import Component


class InterlockingConfiguration(BaseModel):
    """Ths class contains all fiels needed to configure the Interlocking and the RouteController"""

    class Schema(BaseModel.Schema):
        dynamicRouting = marsh.fields.Boolean()

        def _make(self, data: dict) -> "InterlockingConfiguration":
            return InterlockingConfiguration(**data)

    dynamicRouting = BooleanField(default=False)


class RouteController(Component):
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    def next_tick(self, tick: int):
        """This may be called to process a new simulation tick.

        :param tick: The current tick of the simulation.
        :type tick: int
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()


class IInterlockingDisruptor:
    """This class is the Interface to inject faults into the interlocking as well as to notify the Interlocking faults that occur in other parts of the simulation."""

    def insertTrackBlocked(self, track_id: str):
        """This method is used to block a track and recalculate the routes of relevant trains.

        :param track_id: the id of the blocked track
        :type track_id: str
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertTrackUnblocked(self, track_id: str):
        """This method is used to unblock a track and recalculate the routes of relevant trains.

        :param track_id: the id of the unblocked track
        :type track_id: str
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertPlatformBlocked(self, platform_id: str):
        """This method is used to block a platform and recalculate the routes and stops of relevant trains.

        :param platform_id: the id of the blocked platform
        :type platform_id: str
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertPlatformUnblocked(self, platform_id: str):
        """This method is used to unblock a platform and recalculate the routes and stops of relevant trains.

        :param platform_id: the id of the unblocked platform
        :type platform_id: str
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertTrackSpeedLimitChanged(self, track_id: str):
        """This method is used to notify the interlocking about a changed track speed limit, so that it can recalculate the routing of relevant trains.

        :param track_id: the id of the track, which speedlimit changed
        :type track_id: str
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertTrainSpeedChanged(self, train_id: str):
        """This method is used to notify the interlocking about a changed train speed limit, so that it can recalculate the routing of relevant trains.

        :param train_id: the id of the train, which speed limit changed
        :type train_id: str
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()
