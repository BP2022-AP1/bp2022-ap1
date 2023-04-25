import pytest

from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.schedule_blocked_fault import ScheduleBlockedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.spawner.spawner import (
    Spawner,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
)
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from tests.decorators import recreate_db_setup


class TestScheduleBlockedFault:
    """Tests for ScheduleBlockedFault"""

    class MockTraCIWrapper:
        """Mock class for a TraCI wrapper"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def logger(self, run):
        return Logger(run.id)

    @pytest.fixture
    def schedule_blocked_fault_configuration(self, schedule):
        return ScheduleBlockedFaultConfiguration.create(
            **{
                "start_tick": 30,
                "end_tick": 300,
                "description": "test ScheduleBlockedFault",
                "affected_element_id": schedule.id,
            }
        )

    @pytest.fixture
    def schedule_blocked_fault(
        self,
        schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        logger: Logger,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
        spawner: Spawner,
    ):
        return ScheduleBlockedFault(
            configuration=schedule_blocked_fault_configuration,
            logger=logger,
            spawner=spawner,
            simulation_object_updater=simulation_object_updater,
            interlocking=interlocking,
        )

    # It would be better to test if trains spawn after inject_fault.
    # As of now this is not really possible, the tests should therefore edited in the future
    # pylint: disable=protected-access
    def test_inject_schedule_blocked_fault(
        self, tick, schedule_blocked_fault: ScheduleBlockedFault
    ):
        schedule_blocked_fault.inject_fault(tick)
        assert schedule_blocked_fault.spawner.get_schedule(
            schedule_blocked_fault.configuration.affected_element_id
        )._blocked

    def test_resolve_schedule_blocked_fault(
        self, tick, schedule_blocked_fault: ScheduleBlockedFault
    ):
        schedule = schedule_blocked_fault.spawner.get_schedule(
            schedule_blocked_fault.configuration.affected_element_id
        )
        schedule.block()
        assert schedule._blocked
        schedule_blocked_fault.resolve_fault(tick=tick)
        assert not schedule._blocked
