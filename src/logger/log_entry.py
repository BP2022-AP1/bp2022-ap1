from datetime import datetime

import marshmallow as marsh
from peewee import DateTimeField, ForeignKeyField, IntegerField, TextField, UUIDField

from src.base_model import BaseModel
from src.fault_injector.fault_types.platform_blocked_fault import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.train_cancelled_fault import (
    TrainCancelledFaultConfiguration,
)
from src.fault_injector.fault_types.train_speed_fault import (
    TrainSpeedFaultConfiguration,
)
from src.implementor.models import Run


class LogEntry(BaseModel):
    """Represents a single log entry. Used to log messages from the simulation."""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for the LogEntry model."""

        timestamp = marsh.fields.DateTime(required=True)
        tick = marsh.fields.Integer(required=True)
        message = marsh.fields.String(required=True)
        run_id = marsh.fields.UUID(required=True)

        def _make(self, data: dict) -> "LogEntry":
            return LogEntry(**data)

    timestamp = DateTimeField(null=False, default=datetime.now())
    tick = IntegerField(null=False)
    message = TextField(null=False)
    run_id = ForeignKeyField(Run, null=False)


class TrainSpawnLogEntry(LogEntry):
    """A LogEntry that represents the spawning of a train."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainSpawnLogEntry model."""

        train_id = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "TrainSpawnLogEntry":
            return TrainSpawnLogEntry(**data)

    train_id = TextField(null=False)


class TrainRemoveLogEntry(LogEntry):
    """A LogEntry that represents the removal of a train."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainRemoveLogEntry model."""

        train_id = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "TrainRemoveLogEntry":
            return TrainRemoveLogEntry(**data)

    train_id = TextField(null=False)


class TrainArrivalLogEntry(LogEntry):
    """A LogEntry that represents the arrival of a train at a station."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainArrivalLogEntry model."""

        train_id = marsh.fields.String(required=True)
        station_id = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "TrainArrivalLogEntry":
            return TrainArrivalLogEntry(**data)

    train_id = TextField(null=False)
    station_id = TextField(null=False)


class TrainDepartureLogEntry(LogEntry):
    """A LogEntry that represents the departure of a train from a station."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainDepartureLogEntry model."""

        train_id = marsh.fields.String(required=True)
        station_id = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "TrainDepartureLogEntry":
            return TrainDepartureLogEntry(**data)

    train_id = TextField(null=False)
    station_id = TextField(null=False)


class CreateFahrstrasseLogEntry(LogEntry):
    """A LogEntry that represents the creation of a fahrstrasse."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the CreateFahrstrasseLogEntry model."""

        fahrstrasse = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "CreateFahrstrasseLogEntry":
            return CreateFahrstrasseLogEntry(**data)

    fahrstrasse = TextField(null=False)


class RemoveFahrstrasseLogEntry(LogEntry):
    """A LogEntry that represents the removal of a fahrstrasse."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the RemoveFahrstrasseLogEntry model."""

        fahrstrasse = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "RemoveFahrstrasseLogEntry":
            return RemoveFahrstrasseLogEntry(**data)

    fahrstrasse = TextField(null=False)


class SetSignalLogEntry(LogEntry):
    """A LogEntry that represents the setting of a signal."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the SetSignalLogEntry model."""

        signal_id = marsh.fields.UUID(required=True)
        state_before = marsh.fields.Integer(required=True)
        state_after = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "SetSignalLogEntry":
            return SetSignalLogEntry(**data)

    signal_id = UUIDField(null=False)
    state_before = IntegerField(null=False)
    state_after = IntegerField(null=False)


class InjectFaultLogEntry(LogEntry):
    """A LogEntry that represents the injection of a fault."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the InjectFaultLogEntry model."""

        train_speed_fault_configuration = marsh.fields.UUID(required=False)
        platform_blocked_fault_configuration = marsh.fields.UUID(required=False)
        train_cancelled_fault_configuration = marsh.fields.UUID(required=False)
        affected_element = marsh.fields.String(required=True)
        value_before = marsh.fields.String()
        value_after = marsh.fields.String()

        def _make(self, data: dict) -> "InjectFaultLogEntry":
            return InjectFaultLogEntry(**data)

    train_speed_fault_configuration = ForeignKeyField(
        TrainSpeedFaultConfiguration, null=True
    )
    platform_blocked_fault_configuration = ForeignKeyField(
        PlatformBlockedFaultConfiguration, null=True
    )
    train_cancelled_fault_configuration = ForeignKeyField(
        TrainCancelledFaultConfiguration, null=True
    )
    affected_element = TextField(null=False)
    value_before = TextField(null=True)
    value_after = TextField(null=True)


class ResolveFaultLogEntry(LogEntry):
    """A LogEntry that represents the resolving of a fault."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the ResolveFaultLogEntry model."""

        train_speed_fault_configuration = marsh.fields.UUID(required=False)
        platform_blocked_fault_configuration = marsh.fields.UUID(required=False)
        train_cancelled_fault_configuration = marsh.fields.UUID(required=False)

        def _make(self, data: dict) -> "ResolveFaultLogEntry":
            return ResolveFaultLogEntry(**data)

    train_speed_fault_configuration = ForeignKeyField(
        TrainSpeedFaultConfiguration, null=True
    )
    platform_blocked_fault_configuration = ForeignKeyField(
        PlatformBlockedFaultConfiguration, null=True
    )
    train_cancelled_fault_configuration = ForeignKeyField(
        TrainCancelledFaultConfiguration, null=True
    )
