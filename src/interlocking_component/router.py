class Router:
    """This class calculates routes for trains from track segment to track segment."""

    def get_route(self, start_track_segment: "Track", end_track_segment: "Track"):
        """This method returns a route from a start track_segment to an end track_segment.

        :param start_track_segment: The track segment where the route will begin.
        :type start_track_segment: Track
        :param end_track_segment_id: The track segment where the route will end.
        :type end_track_segment: Track
        """
        raise NotImplementedError()
