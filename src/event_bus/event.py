from dataclasses import dataclass
from enum import Enum, auto


class EventType(Enum):
    """represents an EventType"""

    TRAIN_SPAWN = auto()
    TRAIN_REMOVE = auto()
    TRAIN_ARRIVAL = auto()
    TRAIN_DEPARTURE = auto()
    CREATE_FAHRSTRASSE = auto()
    REMOVE_FAHRSTRASSE = auto()
    SET_SIGNAL = auto()
    TRAIN_ENTER_EDGE = auto()
    TRAIN_LEAVE_EDGE = auto()
    INJECT_FAULT = auto()
    RESOLVE_FAULT = auto()


@dataclass
class Event:
    """represents an Event"""

    event_type: EventType
    arguments: dict[str, object]
