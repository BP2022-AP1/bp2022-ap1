import os
from time import sleep
from unittest.mock import patch

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
        traci.vehicle, "getAllSubscriptionResults", get_all_subscription_results
    )
    monkeypatch.setattr(traci, "simulationStep", simulation_step)
    monkeypatch.setattr(traci, "start", start)
    monkeypatch.setattr(traci, "close", close)


# Tests skipped, because the fixtures of celery aren't working properly
# That's why we have to use the real celery app instead and cannot mock the components
@pytest.mark.usefixtures("celery_session_app")
@pytest.mark.usefixtures("celery_session_worker")
@pytest.mark.skip(reason="Celery fixtures are not working properly")
class TestCommunicator:
    def test_simulation_runs(mock_traci):  # pylint: disable=unused-argument
        communicator = Communicator()
        run_id = communicator.run()

        while Communicator.state(run_id) != "PROGRESS":
            if Communicator.state(run_id) == "FAILURE":
                assert False
            sleep(1)
        Communicator.stop(run_id)
        assert Communicator.progress(run_id) > 0


@patch("src.component.MockComponent.next_tick")
def test_component_next_tick_is_called(
    next_tick_mock,
    mock_traci,
):  # pylint: disable=unused-argument
    mock = MockComponent()
    communicator = Communicator(
        components=[mock],
        sumo_configuration=os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        ),
    )
    run_id = communicator.run()
    while Communicator.state(run_id) != "PROGRESS":
        if Communicator.state(run_id) == "FAILURE":
            assert False
        sleep(1)
    Communicator.stop(run_id)
    assert next_tick_mock.assert_called


@patch("src.component.MockComponent.next_tick")
def test_component_next_tick_is_called_add(
    next_tick_mock,
    mock_traci,
):  # pylint: disable=unused-argument
    mock = MockComponent()
    communicator = Communicator(
        sumo_configuration=os.path.join(
            "data", "sumo", "example", "sumo-config", "example.scenario.sumocfg"
        ),
    )
    communicator.add_component(mock)
    run_id = communicator.run()
    while Communicator.state(run_id) != "PROGRESS":
        if Communicator.state(run_id) == "FAILURE":
            assert False
        sleep(1)
    Communicator.stop(run_id)
    assert next_tick_mock.assert_called


@patch("src.communicator.communicator.Communicator._run_with_gui")
def test_run_with_gui_is_called(
    run_with_gui_mock,
):  # pylint: disable=unused-argument
    """
    This test verifies that not the run method connected to celery is executed.
    Instead we should call _run_with_gui.
    """
    os.environ["DISABLE_CELERY"] = "True"
    communicator = Communicator()
    communicator.run()
    del os.environ["DISABLE_CELERY"]
    assert run_with_gui_mock.called


@patch("src.communicator.communicator.run_simulation_steps")
def test_run_simulation_step_is_called_with_gui(
    run_with_gui_mock,
    mock_traci,
):  # pylint: disable=unused-argument
    """
    This test verifies that we call run_simulation_steps when running the simulation in gui mode.
    That run_simulation_steps works correctly is tested in test_component_next_tick_is_called.
    """
    os.environ["DISABLE_CELERY"] = "True"
    communicator = Communicator()
    communicator.run()
    del os.environ["DISABLE_CELERY"]
    assert run_with_gui_mock.called


def test_components_are_ordered_correctly():
    communicator = Communicator()
    mock1 = MockComponent()
    mock2 = MockComponent()
    mock2.priority = 100

    communicator.add_component(mock1)
    communicator.add_component(mock2)

    assert communicator._components == [mock2, mock1]
