import pytest
from interlocking.interlockinginterface import Interlocking

from src.interlocking_component.route_controller import RouteController


class TestRouteController:
    """This tests the route controller"""

    @pytest.fixture
    def route_controller(self) -> RouteController:
        return RouteController()

    def test_start_interlocking(self, route_controller):
        route_controller.start_interlocking("test_example.ppxml")
        assert isinstance(route_controller.interlocking, Interlocking)
