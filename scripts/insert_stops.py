import os
from copy import copy
from typing import Dict

from sumolib import xml

duration = "100"
basepath = os.path.join("data", "sumo", "schwarze_pumpe_v1", "sumo-config")

additionals_file = os.path.join(basepath, "schwarze_pumpe_v1.add.xml")
routes_file = os.path.join(basepath, "schwarze_pumpe_v1.routes.xml")

stations = xml.parse(additionals_file, ["busStop"])
routes = xml.parse(routes_file, ["route"])

mapped_stations: Dict[str, str] = {}

for station in stations:
    mapped_stations[station.id] = station.lane.split("_")[0]

selected_routes = []

for route in routes:
    for station, edge in mapped_stations.items():
        if edge in route.edges.split():
            # we need to duplicate the route
            selected_routes.append((route, station))

routes = next(xml.parse(routes_file, "routes"))
for route, stop in selected_routes:
    child = routes.addChild(
        "route", {"id": route.id + "-" + stop, "edges": route.edges}
    )

    child.addChild("stop", {"busStop": stop, "duration": duration})

with open(routes_file, "w") as modified_routes:
    modified_routes.write(routes.toXML())
