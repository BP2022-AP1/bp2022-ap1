class Route_Controller(Component):
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    def next_tick(self, tick: int):
        """This may be called to prosses a new simulation tick.

        Args:
            tick (int): The current tick of the simulation.

        Raises:
            NotImplementedError: This has not been Implemented yet.
        """
        raise NotImplementedError()
