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
