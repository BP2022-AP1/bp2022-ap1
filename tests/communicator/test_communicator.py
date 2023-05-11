from time import sleep
from unittest.mock import patch

import os

import pytest
import traci

from src.communicator.communicator import Communicator
from src.component import MockComponent


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


def test_simulation_runs(mock_traci):  # pylint: disable=unused-argument
    communicator = Communicator(sumo_configuration = os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        ),)
    run_id = communicator.run()

    while Communicator.state(run_id) != "PROGRESS":
        sleep(1)
    Communicator.stop(run_id)
    assert Communicator.progress(run_id) > 0


@patch("src.component.MockComponent.next_tick")
def test_component_next_tick_is_called(
    next_tick_mock,
    mock_traci,
):  # pylint: disable=unused-argument
    mock = MockComponent()
    communicator = Communicator(components=[mock], sumo_configuration = os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        ),)
    run_id = communicator.run()
    while Communicator.state(run_id) != "PROGRESS":
        sleep(1)
    Communicator.stop(run_id)
    assert next_tick_mock.assert_called


@patch("src.component.MockComponent.next_tick")
def test_component_next_tick_is_called_late_add(
    next_tick_mock,
    mock_traci,
):  # pylint: disable=unused-argument
    mock = MockComponent()
    communicator = Communicator(sumo_configuration = os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        ),)
    communicator.add_component(mock)
    run_id = communicator.run()
    while Communicator.state(run_id) != "PROGRESS":
        sleep(1)
    Communicator.stop(run_id)
    assert next_tick_mock.assert_called
