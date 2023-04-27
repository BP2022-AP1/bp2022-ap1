import os

from interlocking.interlockinginterface import Interlocking

from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)


class TestRouteController:
    """This tests the route controller"""

    def test_start_interlocking(self, route_controller):
        assert isinstance(route_controller.interlocking, Interlocking)
