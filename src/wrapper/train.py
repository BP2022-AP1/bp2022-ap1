from simualtion_object import SimulationObject
from traci import constants, vehicle


class Train(SimulationObject):
    _position = None
    _route: str = None
    _track_id: str = None
    _vehicle_type: str = None
    _speed: float = None
    _max_speed: float = None
    timetable: object = None

    @property
    def track_id(self) -> str:
        """Returns the current track the train is on

        :return: _description_
        """
        return self._track_id

    @property
    def position(self):
        return self._position

    @property
    def speed(self):
        return self._speed

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
        vehicle.setRouteID(self.traci_id, route)
        self._route = route

    @property
    def max_speed(self) -> float:
        return self._max_speed

    @max_speed.setter
    def max_speed(self, speed) -> None:
        vehicle.setMaxSpeed(self.traci_id, speed)
        self._max_speed = speed

    def __init__(self, from_traci: bool = False, *args, **kwargs):
        SimulationObject.__init__(self, *args, **kwargs)

    def _add_to_simulation(self, route_id: str, vehicle_type: str):
        vehicle.add("asdf", route_id, vehicle_type)

    def update(self, updates: dict):
        self._position = updates[constants.VAR_POSITION]
        self._track_id = updates[constants.VAR_ROAD_ID]
        self._route = updates[constants.VAR_ROUTE]
        self._speed = updates[constants.VAR_SPEED]
        self._max_speed = updates[constants.VAR_MAXSPEED]

    def add_subscriptions(self) -> int:
        return (
            constants.VAR_POSITION
            + constants.VAR_ROUTE
            + constants.VAR_ROAD_ID
            + constants.VAR_SPEED
            + constants.VAR_MAXSPEED
        )


class Node(SimulationObject):
    pass


class Signal(Node):
    pass


class Switch(Node):
    pass


class Track(SimulationObject):
    pass
