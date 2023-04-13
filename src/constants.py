from typing import Type

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    InjectFaultLogEntry,
    LogEntry,
    RemoveFahrstrasseLogEntry,
    ResolveFaultLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.spawner.spawner import SpawnerConfiguration, SpawnerConfigurationXSchedule

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
    InjectFaultLogEntry,
    ResolveFaultLogEntry,
    TrackBlockedFaultConfiguration,
    TrainPrioFaultConfiguration,
    TrackSpeedLimitFaultConfiguration,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
]
