import os

import pytest
from interlocking.interlockinginterface import Interlocking

from src.interlocking_component.route_controller import RouteController


class TestRouteController:
    """This tests the route controller"""

    @pytest.fixture
    def route_controller(self) -> RouteController:
        return RouteController(os.path.join("data", "planpro", "test_example.ppxml"))

    def test_start_interlocking(self, route_controller):
        assert isinstance(route_controller.interlocking, Interlocking)
