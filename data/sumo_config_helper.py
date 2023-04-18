import os

from planpro_importer.reader import PlanProReader
from railwayroutegenerator.routegenerator import RouteGenerator
from sumoexporter import SUMOExporter
from track_signal_generator import TrackSignalGenerator


def generate_sumo():
    # Import from local PlanPro file
    topology = PlanProReader(
        "data/planpro/test_with_fixed_points.ppxml"
    ).read_topology_from_plan_pro_file()

    # Generate Signals
    # I'm not sure if this is necessary, but better save than sorry.
    TrackSignalGenerator(topology).place_edge_signals()

    # Generate Routes
    # I'm not sure if this is necessary, but better save than sorry.
    RouteGenerator(topology).generate_routes()

    # Generate the Sumo files
    # chdir is necessary, because sumo_exporter.write_output() is hardcoded to always wirte to the path "sumo-config"
    current_directory = os.getcwd()
    os.makedirs("data/sumo/" + topology.name.split("/")[-1], exist_ok=True)
    os.chdir("data/sumo/" + topology.name.split("/")[-1])
    topology.name = topology.name.split("/")[-1]
    sumo_exporter = SUMOExporter(topology)
    sumo_exporter.convert()
    sumo_exporter.write_output()
    os.chdir(current_directory)


if __name__ == "__main__":
    generate_sumo()
