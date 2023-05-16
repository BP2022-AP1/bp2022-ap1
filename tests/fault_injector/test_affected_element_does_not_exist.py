from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.event_bus.event_bus import EventBus
from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.fault_injector.fault_types.platform_blocked_fault import PlatformBlockedFault
from src.fault_injector.fault_types.schedule_blocked_fault import ScheduleBlockedFault
from src.fault_injector.fault_types.track_blocked_fault import TrackBlockedFault
from src.fault_injector.fault_types.track_speed_limit_fault import TrackSpeedLimitFault
from src.fault_injector.fault_types.train_prio_fault import TrainPrioFault
from src.fault_injector.fault_types.train_speed_fault import TrainSpeedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.spawner.spawner import Spawner
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "table_class, fault_type, object_as_dict",
    [
        [
            TrainSpeedFaultConfiguration,
            TrainSpeedFault,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrainSpeedFault",
                "affected_element_id": "12345678",
                "new_speed": 40,
                "strategy": "regular",
            },
        ],
        [
            PlatformBlockedFaultConfiguration,
            PlatformBlockedFault,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "PlatformBlockedFault",
                "affected_element_id": "12345678",
                "strategy": "regular",
            },
        ],
        [
            TrackBlockedFaultConfiguration,
            TrackBlockedFault,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrackBlockedFault",
                "affected_element_id": "12345678",
                "strategy": "regular",
            },
        ],
        [
            TrainPrioFaultConfiguration,
            TrainPrioFault,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrainPrioFault",
                "affected_element_id": "12345678",
                "new_prio": 1,
                "strategy": "regular",
            },
        ],
        [
            TrackSpeedLimitFaultConfiguration,
            TrackSpeedLimitFault,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrackSpeedLimitFault",
                "affected_element_id": "12345678",
                "new_speed_limit": 60,
                "strategy": "regular",
            },
        ],
    ],
)
class TestAffectedElementDoesNotExist:
    """Test cases where the requested element for injecting a fault does not exist (in the simulation)"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def fault_configuration(self, table_class: BaseModel, object_as_dict: dict):
        return table_class.create(**object_as_dict)

    @pytest.fixture
    def fault(
        self,
        fault_configuration: FaultConfiguration,
        event_bus: EventBus,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
        fault_type: Fault,
    ):
        return fault_type(
            configuration=fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=simulation_object_updater,
            interlocking=interlocking,
        )

    def test_injection(self, tick, fault: Fault):
        with pytest.raises(ValueError):
            fault.inject_fault(tick)

    def test_resolve_without_inject(self, tick, fault: Fault):
        with pytest.raises(ValueError):
            fault.resolve_fault(tick)


class TestAffectedElementDoesNotExistScheduleBlockedFault:
    """Tests cases where the requested element for injecting a schedule blocked fault does not exist (in the simulation)"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def schedule_blocked_fault_configuration(self):
        return ScheduleBlockedFaultConfiguration(
            **{
                "start_tick": 1,
                "end_tick": 100,
                "description": "ScheduleBlockedFault",
                "affected_element_id": "12345678",
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def schedule_blocked_fault(
        self,
        schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        event_bus: EventBus,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
        spawner: Spawner,
    ):
        return ScheduleBlockedFault(
            configuration=schedule_blocked_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=simulation_object_updater,
            interlocking=interlocking,
            spawner=spawner,
        )

    def test_injection(self, tick, schedule_blocked_fault: ScheduleBlockedFault):
        with pytest.raises(KeyError):
            schedule_blocked_fault.inject_fault(tick)

    def test_resolve_without_inject(
        self, tick, schedule_blocked_fault: ScheduleBlockedFault
    ):
        with pytest.raises(KeyError):
            schedule_blocked_fault.resolve_fault(tick)
