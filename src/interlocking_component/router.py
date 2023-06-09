from typing import Dict, List

from src.wrapper.simulation_objects import Edge, Node


class Router:
    """This class calculates routes for trains from edge to edge."""

    def get_route(self, start_edge: Edge, end_edge: Edge) -> List[Node]:
        """This method returns a route from a start edge to an end edge.
        It returns a list of Sumo Nodes from the Node behind the train
        toward to the Node right after the end edge.

        :param start_edge: The edge where the route will begin.
        :type start_edge: Edge
        :param end_edge: The edge where the route will end.
        :type end_edge: Edge
        :return: list of Nodes from the Signal after the start edge
        to the Node right after the end edge
        :rtype: List[Node]
        """
        # The next part is dijkstra as a first mvp.
        # This will lead to deadlocks if two trains drive in opposite directions.
        distances: Dict[Node, int] = {}
        previous_nodes: Dict[Node, Node] = {}
        distances[start_edge.to_node] = 0
        previous_nodes[start_edge.to_node] = start_edge.from_node
        current_index = 0
        while True:
            sorted_distances = sorted(distances.items(), key=lambda item: item[1])
            # This sorts the distances based on the values in the dict.
            # sorted_distances is a array of the dict with items of the dict as tupels.
            try:
                current_node = sorted_distances[current_index][0]
            except Exception as exc:
                raise ValueError("No route could be found.") from exc
            if current_node == end_edge.from_node:
                break
            edge_to_current_node = previous_nodes[current_node].get_edge_to(
                current_node
            )
            for edge in current_node.get_edges_accessible_from(edge_to_current_node):
                if edge.blocked is True:
                    continue
                distance_to_next_node = distances[current_node] + edge.length
                if (
                    edge.to_node not in distances
                    or distances[edge.to_node] > distance_to_next_node
                ):
                    distances[edge.to_node] = distance_to_next_node
                    previous_nodes[edge.to_node] = current_node
            current_index += 1
        route = [end_edge.from_node, end_edge.to_node]
        while current_node in previous_nodes:
            previous_node = previous_nodes[current_node]
            route.insert(0, previous_node)
            current_node = previous_node
            if current_node == start_edge.to_node:
                route.insert(0, previous_nodes[current_node])
                break
        return route
