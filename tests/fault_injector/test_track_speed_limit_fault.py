from src.fault_injector.fault_types.track_speed_limit_fault import TrackSpeedLimitFault, TrackSpeedLimitFaultConfiguration
from src.wrapper.simulation_object_updating_component import SimulationObjectUpdatingComponent
from src.wrapper.simulation_objects import Track
import pytest

class TestTrackSpeedLimitFault:

    @pytest.fixture
    def track():
        return Track("fault injector track")

    @pytest.fixture
    def wrapper(self, monkeypatch):
        new_wrapper = SimulationObjectUpdatingComponent()
        monkeypatch.setattr()
        return SimulationObjectUpdatingComponent()
    
    
