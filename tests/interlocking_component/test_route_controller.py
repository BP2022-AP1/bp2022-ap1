import os

from interlocking.interlockinginterface import Interlocking

from src.interlocking_component.route_controller import RouteController


class TestRouteController:
    """This tests the route controller"""

    def test_start_interlocking(self, route_controller):
        assert isinstance(route_controller.interlocking, Interlocking)
