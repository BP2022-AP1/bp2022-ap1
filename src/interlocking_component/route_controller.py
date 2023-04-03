class RouteController:
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    def check_if_new_fahrstrasse_is_needed(self, train_id: str, track_segment_id: str):
        """This method should be called when a train enters a new track_segment.
        It then checks if the train is near the end of his fahrstrasse and updates it, if necessary.

        :param train_id: the id of the train that may need a new fahrstasse
        :type train_id: train_id
        :param track_segment_id: the id of the tracksegment it just entered
        :type track_segment_id: track_segment_id
        """
        raise NotImplementedError()

    def check_all_fahrstrassen_for_failures(self):
        """This method checks for all trains, if their fahrstrassen and routes are still valid."""
        raise NotImplementedError()


class IInterlockingDisruptor:
    """This class is the Interface to inject faults into the interlocking as well as to notify the Interlocking faults that occur in other parts of the simulation."""

    def insertTrackBlocked(self, track_id: str):
        """This method is used to block a track and recalculate the routes of relevant trains.

        :param track_id: the id of the blocked track
        :type track_id: str
        """
        raise NotImplementedError()

    def insertTrackUnblocked(self, track_id: str):
        """This method is used to unblock a track and recalculate the routes of relevant trains.

        :param track_id: the id of the unblocked track
        :type track_id: str
        """
        raise NotImplementedError()

    def insertPlatformBlocked(self, platform_id: str):
        """This method is used to block a platform and recalculate the routes and stops of relevant trains.

        :param platform_id: the id of the blocked platform
        :type platform_id: str
        """
        raise NotImplementedError()

    def insertPlatformUnblocked(self, platform_id: str):
        """This method is used to unblock a platform and recalculate the routes and stops of relevant trains.

        :param platform_id: the id of the unblocked platform
        :type platform_id: str
        """
        raise NotImplementedError()

    def insertTrackSpeedLimitChanged(self, track_id: str):
        """This method is used to notify the interlocking about a changed track speed limit, so that it can recalculate the routing of relevant trains.

        :param track_id: the id of the track, which speedlimit changed
        :type track_id: str
        """
        raise NotImplementedError()

    def insertTrainSpeedChanged(self, train_id: str):
        """This method is used to notify the interlocking about a changed train speed limit, so that it can recalculate the routing of relevant trains.

        :param train_id: the id of the train, which speed limit changed
        :type train_id: str
        """
        raise NotImplementedError()
