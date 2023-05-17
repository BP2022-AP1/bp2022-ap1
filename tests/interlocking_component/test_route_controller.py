from interlocking.interlockinginterface import Interlocking


class TestRouteController:
    """This tests the route controller"""

    def test_start_interlocking(self, route_controller):
        assert isinstance(route_controller.interlocking, Interlocking)
