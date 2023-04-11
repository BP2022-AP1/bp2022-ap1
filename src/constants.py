from typing import Type

from src.base_model import BaseModel
from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.track_blocked_fault import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.track_speed_limit_fault import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_types.train_cancelled_fault import (
    TrainCancelledFaultConfiguration,
)
from src.fault_injector.fault_types.train_prio_fault import TrainPrioFaultConfiguration
from src.fault_injector.fault_types.train_speed_fault import (
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

# Add classes that should be created as tables to this list
tables: list[Type[BaseModel]] = [
    Run,
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
    SimulationConfiguration,
    Token,
    TrainSpeedFaultConfiguration,
    PlatformBlockedFaultConfiguration,
    TrainCancelledFaultConfiguration,
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
]
