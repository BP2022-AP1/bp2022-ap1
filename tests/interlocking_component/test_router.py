import pytest

from src.interlocking_component.router import Router
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Edge


class TestRouter:
    """This class tests the router."""

    def test_get_route(
        self, router: Router, configured_souc: SimulationObjectUpdatingComponent
    ):
        start_edge: Edge = None
        end_edge: Edge = None
        for edge in configured_souc.edges:
            if edge.identifier == "bf53d-0":
                start_edge = edge
            if edge.identifier == "8f9a9-1":
                end_edge = edge
        route = router.get_route(start_edge, end_edge)
        real_route = [
            "fcb82",
            "94a6f92a-0c2a-40dc-87d6-ccd0e55bf53d-km-25-in",
            "f7d38",
            "7448e",
            "8710dd8c-f9cc-4674-9956-197809e8f9a9-km-25-gegen",
            "8710dd8c-f9cc-4674-9956-197809e8f9a9-km-175-in",
        ]
        assert len(route) == len(real_route)
        for i, id in enumerate(real_route):
            assert route[i].identifier == id

    def test_impossible_route(
        self, router: Router, configured_souc: SimulationObjectUpdatingComponent
    ):
        start_edge: Edge = None
        end_edge: Edge = None
        for edge in configured_souc.edges:
            if edge.identifier == "bf53d-0":
                start_edge = edge
            if edge.identifier == "e346e-1-re":
                end_edge = edge
        with pytest.raises(ValueError):
            router.get_route(start_edge, end_edge)
