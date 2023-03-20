import pytest
import traci

from bp2022_ap1.wrapper.communicator import Communicator


def test_sumo_starts():
    communicator = Communicator()
    communicator.start()

    assert traci.getConnection() is not None

    communicator.stop()


def test_sumo_stops():
    communicator = Communicator()
    communicator.start()
    communicator.stop()

    with pytest.raises(traci.TraCIException):
        traci.getConnection()


def test_sumo_steps_simulation():
    communicator = Communicator()
    communicator.start()
    communicator.simulation_step()

    assert traci.simulation.getTime() == 1.0

    communicator.stop()
