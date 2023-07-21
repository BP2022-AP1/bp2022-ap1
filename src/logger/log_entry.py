from datetime import datetime

from peewee import (
    BigIntegerField,
    DateTimeField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    TextField,
)

from src.base_model import BaseModel
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
from src.implementor.models import Run


class LogEntry(BaseModel):
    """Represents a single log entry. Used to log messages from the simulation."""

    timestamp = DateTimeField(null=False, default=datetime.now())
    tick = BigIntegerField(null=False)
    message = TextField(null=False)
    run_id = ForeignKeyField(Run, null=False)


class TrainSpawnLogEntry(LogEntry):
    """A LogEntry that represents the spawning of a train."""

    train_id = TextField(null=False)


class TrainRemoveLogEntry(LogEntry):
    """A LogEntry that represents the removal of a train."""

    train_id = TextField(null=False)


class TrainArrivalLogEntry(LogEntry):
    """A LogEntry that represents the arrival of a train at a station."""

    train_id = TextField(null=False)
    station_id = TextField(null=False)


class TrainDepartureLogEntry(LogEntry):
    """A LogEntry that represents the departure of a train from a station."""

    train_id = TextField(null=False)
    station_id = TextField(null=False)


class CreateFahrstrasseLogEntry(LogEntry):
    """A LogEntry that represents the creation of a fahrstrasse."""

    fahrstrasse = TextField(null=False)


class RemoveFahrstrasseLogEntry(LogEntry):
    """A LogEntry that represents the removal of a fahrstrasse."""

    fahrstrasse = TextField(null=False)


class SetSignalLogEntry(LogEntry):
    """A LogEntry that represents the setting of a signal."""

    signal_id = TextField(null=False)
    state_before = IntegerField(null=False)
    state_after = IntegerField(null=False)


class TrainEnterEdgeLogEntry(LogEntry):
    """A LogEntry that represents the entry of a train into an edge."""

    train_id = TextField(null=False)
    edge_id = TextField(null=False)
    edge_length = FloatField(null=False)


class TrainLeaveEdgeLogEntry(LogEntry):
    """A LogEntry that represents the leaving of a train from an edge."""

    train_id = TextField(null=False)
    edge_id = TextField(null=False)


class InjectFaultLogEntry(LogEntry):
    """A LogEntry that represents the injection of a fault."""

    platform_blocked_fault_configuration = ForeignKeyField(
        PlatformBlockedFaultConfiguration, null=True
    )
    track_blocked_fault_configuration = ForeignKeyField(
        TrackBlockedFaultConfiguration, null=True
    )
    track_speed_limit_fault_configuration = ForeignKeyField(
        TrackSpeedLimitFaultConfiguration, null=True
    )
    schedule_blocked_fault_configuration = ForeignKeyField(
        ScheduleBlockedFaultConfiguration, null=True
    )
    train_prio_fault_configuration = ForeignKeyField(
        TrainPrioFaultConfiguration, null=True
    )
    train_speed_fault_configuration = ForeignKeyField(
        TrainSpeedFaultConfiguration, null=True
    )
    affected_element = TextField(null=False)
    value_before = TextField(null=True)
    value_after = TextField(null=True)


class ResolveFaultLogEntry(LogEntry):
    """A LogEntry that represents the resolving of a fault."""

    platform_blocked_fault_configuration = ForeignKeyField(
        PlatformBlockedFaultConfiguration, null=True
    )
    track_blocked_fault_configuration = ForeignKeyField(
        TrackBlockedFaultConfiguration, null=True
    )
    track_speed_limit_fault_configuration = ForeignKeyField(
        TrackSpeedLimitFaultConfiguration, null=True
    )
    schedule_blocked_fault_configuration = ForeignKeyField(
        ScheduleBlockedFaultConfiguration, null=True
    )
    train_prio_fault_configuration = ForeignKeyField(
        TrainPrioFaultConfiguration, null=True
    )
    train_speed_fault_configuration = ForeignKeyField(
        TrainSpeedFaultConfiguration, null=True
    )
