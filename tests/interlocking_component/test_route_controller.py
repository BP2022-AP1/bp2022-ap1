import os
from uuid import uuid1

import pytest
from interlocking.interlockinginterface import Interlocking

from src.interlocking_component.route_controller import RouteController
from src.logger.logger import Logger


class TestRouteController:
    """This tests the route controller"""

    @pytest.fixture
    def mock_logger(mocker) -> Logger:
        return mocker.Mock(spec=Logger)

    @pytest.fixture
    def route_controller(mock_logger: Logger) -> RouteController:
        return RouteController(
            logger=mock_logger,
            priority=1,
            path_name=os.path.join("data", "planpro", "test_example.ppxml"),
        )

    def test_start_interlocking(self, route_controller):
        assert isinstance(route_controller.interlocking, Interlocking)
