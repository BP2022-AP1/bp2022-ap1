from typing import Type

from src.base_model import BaseModel
from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
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
    PlatformBlockedFaultConfiguration,
]
