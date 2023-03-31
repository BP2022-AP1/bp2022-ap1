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

    def insertTrackBlocked(self, track: track):
        """This method is used to block a track and recalculate the routes of relevant trains.

        :param track: the blocked track
        :type track: track (as a simulation_object)
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertTrackNotBlocked(self, track: track):
        """This method is used to unblock a track and recalculate the routes of relevant trains.

        :param track: the unblocked track
        :type track: track (as a simulation_object)
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertPlatformBlocked(self, platform: platform):
        """This method is used to block a platform and recalculate the routes and stops of relevant trains.

        :param platform: the blocked platform
        :type platform: platform (as a simulation_object)
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertPlatformNotBlocked(self, platform: platform):
        """This method is used to unblock a platform and recalculate the routes and stops of relevant trains.

        :param platform: the unblocked platform
        :type platform: platform (as a simulation_object)
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertTrackSpeedLimitChanged(self, track: track):
        """This method is used to notify the interlocking about a changed track speed limit, so that it can recalculate the routing of relevant trains.

        :param track: the track, which speedlimit changed
        :type track: track (as a simulation_object)
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()

    def insertTrainSpeedChanged(self, train: train):
        """This method is used to notify the interlocking about a changed train speed limit, so that it can recalculate the routing of relevant trains.

        :param train: the train, which speed limit changed
        :type train: train (as a simulation_object)
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()
