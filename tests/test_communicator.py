from bp2022_ap1.wrapper.communicator import Communicator
import traci
import pytest


def test_sumo_starts():
    c = Communicator()
    c.start()

    assert traci.getConnection() is not None

    c.stop()

def test_sumo_stops():
    c = Communicator()
    c.start()
    c.stop()

    with pytest.raises(traci.TraCIException):
        traci.getConnection()

def test_sumo_steps_simulation():
    c = Communicator()
    c.start()
    c.simulation_step()

    assert traci.simulation.getTime() == 1.0

    c.stop()