from typing import Type

from src.base_model import BaseModel
from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.train_speed_fault import (
    TrainSpeedFaultConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule import Schedule
from src.schedule.schedule_strategy import ScheduleStrategy
from src.schedule.train_schedule import TrainSchedule, TrainScheduleXSimulationPlatform

# Add classes that should be created as tables to this list
tables: list[Type[BaseModel]] = [
    Run,
    ScheduleStrategy,
    RegularScheduleStrategy,
    Schedule,
    TrainSchedule,
    TrainScheduleXSimulationPlatform,
    SimulationConfiguration,
    Token,
    TrainSpeedFaultConfiguration,
    PlatformBlockedFaultConfiguration,
]
