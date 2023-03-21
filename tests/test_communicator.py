from time import sleep

from src.wrapper.communicator import Communicator


def test_simulation_runs():
    communicator = Communicator()
    communicator.start()
    sleep(0.1)
    communicator.stop()
    assert communicator.progress > 0