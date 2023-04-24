from time import sleep

import pytest
import traci

from src.communicator.communicator import Communicator
from src.component import Component


@pytest.fixture
def mock_traci(monkeypatch):
    def get_all_subscription_results():
        return {}

    def simulation_step(*args, **kwargs):  # pylint: disable=unused-argument
        return

    def start(*args, **kwargs):  # pylint: disable=unused-argument
        return

    def close(*args, **kwargs):  # pylint: disable=unused-argument
        return

    monkeypatch.setattr(
        traci.simulation, "getAllSubscriptionResults", get_all_subscription_results
    )
    monkeypatch.setattr(traci, "simulationStep", simulation_step)
    monkeypatch.setattr(traci, "start", start)
    monkeypatch.setattr(traci, "close", close)


class MockComponent(Component):
    """Mock for a simple component to check if next tick is called"""

    call_count = 0

    def __init__(self):
        Component.__init__(self, None, 1)

    def next_tick(self, tick: int):
        self.call_count += 1


def test_simulation_runs(
    mock_traci,
):  # pylint: disable=unused-argument
    communicator = Communicator()
    communicator.start()
    sleep(0.1)
    communicator.stop()
    assert communicator.progress > 0


def test_component_next_tick_is_called(
    mock_traci,
):  # pylint: disable=unused-argument
    mock = MockComponent()
    communicator = Communicator(components=[mock])
    communicator.start()
    sleep(0.1)
    communicator.stop()
    assert mock.call_count > 0


def test_component_next_tick_is_called_late_add(
    mock_traci,
):  # pylint: disable=unused-argument
    mock = MockComponent()
    communicator = Communicator()
    communicator.start()
    communicator.add_component(mock)
    sleep(0.1)
    communicator.stop()
    assert mock.call_count > 0
