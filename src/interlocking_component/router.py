from typing import List

from src.wrapper.simulation_objects import Node, Track


class Router:
    """This class calculates routes for trains from track segment to track segment."""

    def get_route(self, start_track: Track, end_track: Track) -> List[Node]:
        """This method returns a route from a start track_segment to an end track_segment.
        It returns a list of Sumo Nodes from the Signal the train is currently driving
        toward to the Node right after the end track.

        :param start_track: The track segment where the route will begin.
        :type start_track: Track
        :param end_track: The track segment where the route will end.
        :type end_track: Track
        :return: list of Nodes from the Signal after the start track
        to the Node right after the end track
        :rtype: List[Node]
        """
        raise NotImplementedError()
