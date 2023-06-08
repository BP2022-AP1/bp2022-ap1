import pytest

from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.schedule_blocked_fault import ScheduleBlockedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.spawner.spawner import Spawner
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
    def schedule_blocked_fault_configuration(self, schedule):
        return ScheduleBlockedFaultConfiguration.create(
            **{
                "start_tick": 30,
                "end_tick": 300,
                "description": "test ScheduleBlockedFault",
                "affected_element_id": schedule.id,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def schedule_blocked_fault(
        self,
        schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        event_bus: EventBus,
        souc: SimulationObjectUpdatingComponent,
        interlocking_disruptor: IInterlockingDisruptor,
        spawner: Spawner,
    ):
        return ScheduleBlockedFault(
            configuration=schedule_blocked_fault_configuration,
            event_bus=event_bus,
            spawner=spawner,
            simulation_object_updater=souc,
            interlocking_disruptor=interlocking_disruptor,
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
