from simualtion_object import SimulationObject
from traci import vehicle, constants

class Train(SimulationObject):

    _traci_id = None

    _position = None
    _route = None
    _road_id = None
    _vehicle_type: str = None

# add(self, vehID, routeID, typeID='DEFAULT_VEHTYPE', depart='now', departLane='first', departPos='base', departSpeed='0', arrivalLane='current', arrivalPos='max', arrivalSpeed='current', fromTaz='', toTaz='', line='', personCapacity=0, personNumber=0)
# changeTarget(self, vehID, edgeID)

    @property
    def road_id(self):
        return self._road_id

    @property
    def position(self):
        return self._position

    @property
    def route(self) -> int:
        """This method returns the current sumo-route-id.

        :return: The route this vehicle is following
        """
        return self._route

    @route.setter
    def route(self, route: int) -> None:
        """This method updates the vehicle route to the given sumo-route.

        :performance consideration: This method makes one traci-roundtrip
        :param route: the route that the vehicle should follow
        """
        vehicle.setRouteID(self._traci_id, route)
        self._route = route

    def __init__(self, *args, **kwargs, from_traci: bool = False):
        SimulationObject.__init__(self, *args, **kwargs)

    def _add_to_simulation(self, route_id: str, vehicle_type: str, departure_time: ):
        vehicle.add("asdf", route_id, vehicle_type)

    def update(self, updates: dict):
        self._position = updates[constants.VAR_POSITION]
        self._road_id = updates[constants.VAR_ROAD_ID]
        self._route = updates[constants.VAR_ROUTE]

    def add_subscriptions(self) -> int:
        return constants.VAR_POSITION + constants.VAR_ROUTE + constants.VAR_ROAD_ID