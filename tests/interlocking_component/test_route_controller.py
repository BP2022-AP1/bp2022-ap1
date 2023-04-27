import os

import pytest
from interlocking.interlockinginterface import Interlocking

from src.interlocking_component.route_controller import RouteController
from src.wrapper.simulation_object_updating_component import SimulationObjectUpdatingComponent


class TestRouteController:
    """This tests the route controller"""
    
    @pytest.fixture
    def mock_simulation_object_updating_component(mocker) -> SimulationObjectUpdatingComponent:
        return mocker.Mock(spec=SimulationObjectUpdatingComponent)

    @pytest.fixture
    def route_controller(mock_simulation_object_updating_component: SimulationObjectUpdatingComponent) -> RouteController:
        return RouteController(
            simulation_object_updating_component=mock_simulation_object_updating_component,
            path_name=os.path.join("data", "planpro", "test_example.ppxml"),
        )

    def test_start_interlocking(self, route_controller):
        assert isinstance(route_controller.interlocking, Interlocking)
