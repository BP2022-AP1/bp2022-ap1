from orm_importer.importer import ORMImporter
from planproexporter import Generator
from railwayroutegenerator.routegenerator import RouteGenerator
from sumoexporter.sumoexporter import SUMOExporter
from track_signal_generator.generator import TrackSignalGenerator

from yaramo.edge import Edge
from yaramo.geo_node import DbrefGeoNode
from yaramo.node import Node
from yaramo.topology import Topology

import os

def setup() -> Topology:
    node1 = Node()
    node2 = Node()
    node5 = Node()
    node7 = Node()
    switch1 = Node()
    switch2 = Node()
    switch3 = Node()
    switch4 = Node()

    node1.geo_node = DbrefGeoNode(000, 10)
    node2.geo_node = DbrefGeoNode(250, 10)
    #node3.geo_node = DbrefGeoNode(250, 20)
    #node4.geo_node = DbrefGeoNode(250, 30)
    node5.geo_node = DbrefGeoNode(350, 20)
    #node6.geo_node = DbrefGeoNode(75, 10)
    node7.geo_node = DbrefGeoNode(000, 00)
    switch1.geo_node = DbrefGeoNode(50, 10)
    switch2.geo_node = DbrefGeoNode(100, 20)
    switch3.geo_node = DbrefGeoNode(100, 10)
    switch4.geo_node = DbrefGeoNode(300, 20)

    edge1 = Edge(node1, switch1, length=50)
    edge1.maximum_speed = 160
    edge2 = Edge(switch1, switch3, length=50)
    edge2.maximum_speed = 160
    #edge3 = Edge(node6, switch3, length=25)
    edge4 = Edge(switch1, switch2, length=50)
    edge4.maximum_speed = 160
    edge5 = Edge(switch3, node7, length=100)
    edge5.maximum_speed = 160
    edge6 = Edge(switch3, node2, length=150)
    edge6.maximum_speed = 160
    edge7 = Edge(switch2, switch4, length=200)
    edge7.maximum_speed = 160
    #edge10 = Edge(node3, switch4, length=50)
    edge8 = Edge(switch2, switch4, length=200)
    edge8.maximum_speed = 160
    #edge9 = Edge(node4, switch4, length=50)
    edge11 = Edge(switch4, node5, length=50)
    edge11.maximum_speed = 160

    edge2.intermediate_geo_nodes.append(DbrefGeoNode(75, 10))
    edge4.intermediate_geo_nodes.append(DbrefGeoNode(75, 20))
    edge5.intermediate_geo_nodes.append(DbrefGeoNode(75, 00))
    edge7.intermediate_geo_nodes.append(DbrefGeoNode(250, 20))
    edge8.intermediate_geo_nodes.append(DbrefGeoNode(125, 30))
    edge8.intermediate_geo_nodes.append(DbrefGeoNode(250, 30))
    edge8.intermediate_geo_nodes.append(DbrefGeoNode(275, 30))

    switch1.set_connection_head_edge(edge2)
    switch1.set_connection_left_edge(edge4)
    switch1.set_connection_right_edge(edge1)

    switch2.set_connection_head_edge(edge7)
    switch2.set_connection_left_edge(edge8)
    switch2.set_connection_right_edge(edge4)

    switch3.set_connection_head_edge(edge2)
    switch3.set_connection_left_edge(edge6)
    switch3.set_connection_right_edge(edge5)

    switch4.set_connection_head_edge(edge7)
    switch4.set_connection_left_edge(edge11)
    switch4.set_connection_right_edge(edge8)
    
    node1.set_connection_head_edge(edge1)

    node2.set_connection_head_edge(edge6)

    node5.set_connection_head_edge(edge11)

    node7.set_connection_head_edge(edge5)

    topology = Topology()
    topology.add_node(node1)
    topology.add_node(node2)
    topology.add_node(node5)
    topology.add_node(node7)
    topology.add_node(switch1)
    topology.add_node(switch2)
    topology.add_node(switch3)
    topology.add_node(switch4)

    topology.add_edge(edge1)
    topology.add_edge(edge2)
    topology.add_edge(edge4)
    topology.add_edge(edge5)
    topology.add_edge(edge6)
    topology.add_edge(edge7)
    topology.add_edge(edge8)
    topology.add_edge(edge11)

    return topology


def generate_files():
    cordinates = [
        (51.5594, 14.3344),
        (51.5381, 14.3794),
        (51.4829, 14.4130),
        (51.5166, 14.3088),
    ]
    polygon = ""
    for cord in cordinates:
        polygon += str(cord[0]) + " "
        polygon += str(cord[1]) + " "
    polygon = polygon[:-1]
    # This is somewhere west of Schwarze Pumpe.

    # Import from OSM/ORM
    #topology = ORMImporter().run(polygon)
    topology = setup()
    topology.name = "example"

    # Generate Signals
    tsg = TrackSignalGenerator(topology)
    tsg.place_switch_signals()
    tsg.place_edge_signals()

    # Generate Routes
    RouteGenerator(topology).generate_routes()

    # Write PlanPro
    generator = Generator()
    generator.generate(
        topology, "BP2022-AP1", "BP2022-AP1", "data/planpro/example"
    )

    current_directory = os.getcwd()
    os.makedirs("data/sumo/" + topology.name.split("/")[-1], exist_ok=True)
    os.chdir("data/sumo/" + topology.name.split("/")[-1])
    topology.name = topology.name.split("/")[-1]
    sumo_exporter = SUMOExporter(topology)
    sumo_exporter.convert()
    sumo_exporter.write_output()
    os.chdir(current_directory)

if __name__ == "__main__":
    generate_files()
