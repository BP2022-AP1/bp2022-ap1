from time import sleep

from src.component import Component
from src.wrapper.communicator import Communicator


class MockComponent(Component):
    """Mock for a simple component to check if next tick is called"""

    call_count = 0

    def __init__(self):
        Component.__init__(self, None, 1)

    def next_tick(self, tick: int):
        self.call_count += 1


def test_simulation_runs():
    communicator = Communicator()
    communicator.start()
    while not communicator.sumo_running:
        sleep(1)
    communicator.stop()
    assert communicator.progress > 0


def test_component_next_tick_is_called():
    mock = MockComponent()
    communicator = Communicator(components=[mock])
    communicator.start()
    while not communicator.sumo_running:
        sleep(1)
    communicator.stop()
    assert mock.call_count > 0


def test_component_next_tick_is_called_late_add():
    mock = MockComponent()
    communicator = Communicator()
    communicator.start()
    communicator.add_component(mock)
    while not communicator.sumo_running:
        sleep(1)
    communicator.stop()
    assert mock.call_count > 0
