from typing import Type

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
    PlatformBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
    TrackBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
    TrainPrioFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
    TrainSpeedFaultConfigurationXSimulationConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
    InterlockingConfigurationXSimulationConfiguration,
)
from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    InjectFaultLogEntry,
    LogEntry,
    RemoveFahrstrasseLogEntry,
    ResolveFaultLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainEnterEdgeLogEntry,
    TrainLeaveEdgeLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.schedule.smard_api import SmardApiEntry, SmardApiIndex
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)

# Add classes that should be created as tables to this list
tables: list[Type[BaseModel]] = [
    Run,
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
    SimulationConfiguration,
    Token,
    TrainSpeedFaultConfiguration,
    PlatformBlockedFaultConfiguration,
    ScheduleBlockedFaultConfiguration,
    LogEntry,
    TrainSpawnLogEntry,
    TrainRemoveLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    CreateFahrstrasseLogEntry,
    RemoveFahrstrasseLogEntry,
    SetSignalLogEntry,
    TrainEnterEdgeLogEntry,
    TrainLeaveEdgeLogEntry,
    InjectFaultLogEntry,
    ResolveFaultLogEntry,
    TrackBlockedFaultConfiguration,
    TrainPrioFaultConfiguration,
    TrackSpeedLimitFaultConfiguration,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    InterlockingConfiguration,
    SpawnerConfigurationXSimulationConfiguration,
    InterlockingConfigurationXSimulationConfiguration,
    TrainPrioFaultConfigurationXSimulationConfiguration,
    TrainSpeedFaultConfigurationXSimulationConfiguration,
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
    PlatformBlockedFaultConfigurationXSimulationConfiguration,
    TrackBlockedFaultConfigurationXSimulationConfiguration,
    SmardApiIndex,
    SmardApiEntry,
]
