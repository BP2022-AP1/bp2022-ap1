from dataclasses import dataclass
from enum import StrEnum, auto


class EventType(StrEnum):
    TrainSpawn = auto()
    TrainRemove = auto()
    TrainArrival = auto()
    TrainDeparture = auto()
    CreateFahrstrasse = auto()
    RemoveFahrstrasse = auto()
    SetSignal = auto()
    TrainEnterBlockSection = auto()
    TrainLeaveBlockSection = auto()
    InjectFault = auto()
    ResolveFault = auto()


@dataclass
class Event:
    event_type: EventType
    arguments: dict[str, object]
