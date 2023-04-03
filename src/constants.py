from typing import Type

from src.base_model import BaseModel
from src.implementor.models import SimulationConfiguration, Run

# Add classes that should be created as tables to this list
tables: list[Type[BaseModel]] = [SimulationConfiguration, Run
