from typing import Type

from src.base_model import BaseModel
from src.implementor.models import Run
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule import Schedule
from src.schedule.schedule_strategy import ScheduleStrategy
from src.schedule.train_schedule import TrainSchedule, TrainScheduleXSimulationPlatform
from src.implementor.models import Run, SimulationConfiguration, Token

# Add classes that should be created as tables to this list
tables: list[Type[BaseModel]] = [
    Run,
    ScheduleStrategy,
    RegularScheduleStrategy,
    Schedule,
    TrainSchedule,
    TrainScheduleXSimulationPlatform,
    SimulationConfiguration, 
    Token
]

tables: list[Type[BaseModel]] = [Run, SimulationConfiguration, Token]
