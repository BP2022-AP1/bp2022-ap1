from typing import List

from src.wrapper.simulation_objects import Node, Edge


class Router:
    """This class calculates routes for trains from track segment to track segment."""

    def get_route(self, start_edge: Edge, end_edge: Edge) -> List[Node]:
        """This method returns a route from a start track_segment to an end track_segment.
        It returns a list of Sumo Nodes from the Signal the train is currently driving
        toward to the Node right after the end track.

        :param start_edge: The edge where the route will begin.
        :type start_edge: Edge
        :param end_edge: The edge where the route will end.
        :type end_edge: Edge
        :return: list of Nodes from the Signal after the start edge
        to the Node right after the end edge
        :rtype: List[Node]
        """
        start_node = start_edge.to_node
        penultimate_node = end_edge.from_node

        # The next part is dijkstra as a first mvp.
        # This will lead to deadlocks if two trains drive in opposite directions.
        distances = {}
        previous_nodes = {}
        distances[start_node] = 0
        current_index = 0
        current_node = start_node
        while True:
            sorted_distances = sorted(distances.items(), key=lambda item: item[1])
            # This sorts the distances based on the values in the dict.
            # sorted_distances is a array of the dict with items of the dict as tupels.

            last_node = current_node
            current_node = sorted_distances[current_index][0]
            previous_nodes[current_node] = last_node
            if current_node == penultimate_node:
                break
            for track in current_node.tracks:
                distance_to_next_node = distances[current_node] + track.length
                if (
                    track.end_node not in distances
                    or distances[track.to_node] < distance_to_next_node
                ):
                    distances[track.to_node] = distance_to_next_node
            current_index += 1
        route = List[penultimate_node, end_edge.to_node]
        while current_node in previous_nodes:
            previous_node = previous_nodes[current_node]
            route.insert(0, previous_node)
            current_node = previous_node
        return route
