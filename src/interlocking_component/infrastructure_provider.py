from interlocking.infrastructureprovider.infrastructureprovider import (
    InfrastructureProvider,
)

from src.wrapper.simulation_objects import Edge, Signal, Switch, Train


class SumoInfrastructureProvider(InfrastructureProvider):
    """This class passes calls from the Interlocking and RouteController to the SimulationObjects.
    It also notifies the Interlocking and the RouteController about the movement of trains.
    """

    route_controller: "RouteController"

    def __init__(
        self,
        route_controller: "RouteController",
    ):
        super().__init__()
        self.route_controller = route_controller
        self.route_controller.simulation_object_updating_component.infrastructur_provider = (
            self
        )

    def turn_point(self, yaramo_point, target_orientation):
        super().turn_point(yaramo_point, target_orientation)
        switch = None
        for (
            potencial_switch
        ) in self.route_controller.simulation_object_updating_component.switches:
            if potencial_switch.identifier == yaramo_point.point_id:
                switch = potencial_switch
                break
        if target_orientation == "left":
            switch.state = Switch.State.LEFT
        elif target_orientation == "right":
            switch.state = Switch.State.RIGHT

    def set_signal_state(self, yaramo_signal, target_state):
        super().set_signal_state(yaramo_signal, target_state)
        signal = None
        for (
            potencial_signal
        ) in self.route_controller.simulation_object_updating_component.signals:
            if potencial_signal.identifier == yaramo_signal.name:
                signal = potencial_signal
                break
        if target_state == "halt":
            signal.state = Signal.State.HALT
        elif target_state == "go":
            signal.state = Signal.State.GO

    def train_drove_onto_track(self, train: Train, edge: Edge):
        """This method calls tds_count_in with the track_segment_id of the given edge
        and calls the route_controller to update the fahrstrasse.

        :param train: The train
        :type train: Train
        :param edge: The edge the train drov onto
        :type edge: Edge
        """
        track_segment_id = edge.identifier.split("-re")[0]
        # The interlocking does not have two edges per track, so the -re must be removed if there
        self.tds_count_in(track_segment_id)

        self.route_controller.maybe_update_fahrstrasse(train, edge)

    def train_drove_off_track(self, edge: Edge):
        """This method calls tds_count_out with the track_segment_id of the given edge.

        :param edge: The edge the train drove off of
        :type edge: Edge
        """
        track_segment_id = edge.identifier.split("-re")[0]
        # The interlocking does not have two edges per track, so the -re must be removed if there
        self.tds_count_out(track_segment_id)

        self.route_controller.maybe_free_fahrstrasse(edge)
