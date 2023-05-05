import uuid
from time import sleep
from unittest.mock import patch

import pytest

from src import implementor as impl
from src.communicator.communicator import Communicator
from src.implementor.models import Run


class TestRunImplementor:
    def test_get_all_simulation_ids(self, token, empty_simulation_configuration):
        run = Run.create(simulation_configuration=empty_simulation_configuration)
        result, status = impl.run.get_all_run_ids({}, token)
        assert status == 200
        assert str(run.id) in result

    def test_get_all_simulation_ids_option(
        self,
        token,
        empty_simulation_configuration,
        another_empty_simulation_configuration,
    ):
        run = Run.create(simulation_configuration=empty_simulation_configuration)
        another_run = Run.create(
            simulation_configuration=another_empty_simulation_configuration
        )
        result, status = impl.run.get_all_run_ids(
            {"simulationId": empty_simulation_configuration.id}, token
        )
        assert status == 200
        assert str(run.id) in result
        assert str(another_run.id) not in result

    def test_get_all_simulation_ids_not_found(self, token):
        result, status = impl.run.get_all_run_ids(
            {"simulationId": str(uuid.uuid4())}, token
        )
        assert status == 404
        assert result == "Simulation not found"

    def create_run_id_not_found(self, token):
        result, status = impl.run.create_run(
            {"simulation_configuration": str(uuid.uuid4())}, token
        )
        assert status == 404
        assert result == "Simulation not found"

    @patch("src.interlocking_component.route_controller.RouteController.next_tick")
    @patch("src.spawner.spawner.Spawner.next_tick")
    @patch(
        "src.fault_injector.fault_types.platform_blocked_fault.PlatformBlockedFault.next_tick"
    )
    @patch(
        "src.fault_injector.fault_types.schedule_blocked_fault.ScheduleBlockedFault.next_tick"
    )
    @patch(
        "src.fault_injector.fault_types.track_blocked_fault.TrackBlockedFault.next_tick"
    )
    @patch(
        "src.fault_injector.fault_types.track_speed_limit_fault.TrackSpeedLimitFault.next_tick"
    )
    @patch("src.fault_injector.fault_types.train_speed_fault.TrainSpeedFault.next_tick")
    @patch("src.fault_injector.fault_types.train_prio_fault.TrainPrioFault.next_tick")
    @patch(
        "src.wrapper.simulation_object_updating_component.SimulationObjectUpdatingComponent.next_tick"
    )
    def test_create_run(
        self,
        route_controller_next_tick_mock,
        spawner_next_tick_mock,
        platform_blocked_fault_next_tick_mock,
        schedule_blocked_fault_next_tick_mock,
        track_blocked_fault_next_tick_mock,
        track_speed_limit_fault_next_tick_mock,
        train_speed_fault_next_tick_mock,
        train_prio_fault_next_tick_mock,
        simulation_object_updating_component_next_tick_mock,
        token,
        simulation_configuration_full,
    ):
        result, status = impl.run.create_run(
            {"simulation_configuration": simulation_configuration_full.id}, token
        )
        assert status == 201
        run_id = result["id"]
        assert Run.select().where(Run.id == run_id).exists()
        run = Run.select().where(Run.id == run_id).get()
        assert run.simulation_configuration.id == simulation_configuration_full.id

        while Communicator.state(str(run.process_id)) != "PROGRESS":
            sleep(1)
        Communicator.stop(str(run.process_id))
        assert route_controller_next_tick_mock.assert_called
        assert spawner_next_tick_mock.assert_called
        assert platform_blocked_fault_next_tick_mock.assert_called
        assert schedule_blocked_fault_next_tick_mock.assert_called
        assert track_blocked_fault_next_tick_mock.assert_called
        assert track_speed_limit_fault_next_tick_mock.assert_called
        assert train_speed_fault_next_tick_mock.assert_called
        assert train_prio_fault_next_tick_mock.assert_called
        assert simulation_object_updating_component_next_tick_mock.assert_called
