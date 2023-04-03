class Router:
    """This class will calculate routes for trains from track segment to track segment."""

    def get_route(self, start_track_segment_id: str, end_track_segment_id: str):
        """This method returns a route from a start track_segment to an end track_segment.

        :param start_track_segment_id: The id of the track segment where the route will begin.
        :type start_track_segment_id: str
        :param end_track_segment_id: The id of the track segment where the route will end.
        :type end_track_segment_id: str
        """
        raise NotImplementedError()
