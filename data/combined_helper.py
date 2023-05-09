from orm_importer.importer import ORMImporter
from planproexporter import Generator
from railwayroutegenerator.routegenerator import RouteGenerator
from track_signal_generator.generator import TrackSignalGenerator

import os
from sumoexporter.sumoexporter import SUMOExporter


def generate_planpro():
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
    topology = ORMImporter().run(polygon)
    topology.name = "debuggingisfun3"

    # Generate Signals
    TrackSignalGenerator(topology).place_edge_signals()

    # Generate Routes
    RouteGenerator(topology).generate_routes()

    # Write PlanPro
    generator = Generator()
    generator.generate(
        topology, "BP2022-AP1", "BP2022-AP1", "data/planpro/" + topology.name
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
    generate_planpro()