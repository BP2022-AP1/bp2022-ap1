from interlocking.infrastructureprovider.infrastructureprovider import InfrastructureProvider
from src.wrapper.simulation_object_updating_component import SimulationObjectUpdatingComponent
from src.wrapper.simulation_objects import Switch, Signal

class SumoInfrastructureProvider(InfrastructureProvider):

    simulation_object_updating_component :SimulationObjectUpdatingComponent

    def __init__(self, simulation_object_updating_component :SimulationObjectUpdatingComponent):
        super.__init__()
        self.simulation_object_updating_component = simulation_object_updating_component

    def turn_point(self, yaramo_point, target_orientation):
        super.turn_point(yaramo_point, target_orientation)
        switch = None
        for potencial_switch in self.simulation_object_updating_component.switches:
            if potencial_switch.identifier == yaramo_point.point_id:
                switch = potencial_switch
                break
        if target_orientation == "left":
            switch.state = Switch.State.LEFT
        elif target_orientation == "right":
            switch.state = Switch.State.RIGHT

    def set_signal_state(self, yaramo_signal, target_state):
        super.set_signal_state(self, yaramo_signal, target_state)
        signal = None
        for potencial_signal in self.simulation_object_updating_component.signals:
            if potencial_signal.identifier == yaramo_signal.name:
                signal = potencial_signal
                break
        if target_state == "halt":
            signal.state = Signal.State.HALT
        elif target_state == "right":
            signal.state = Signal.State.GO