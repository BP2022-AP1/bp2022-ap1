import marshmallow as marsh
from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField

from src.base_model import BaseModel
from src.implementor.models import Run


class LogEntry(BaseModel):
    """Represents a single log entry. Used to log messages from the simulation."""

    class Schema(BaseModel.Schema):
        """The marshmallow schema for the LogEntry model."""

        timestamp = marsh.fields.DateTime(required=True)
        message = marsh.fields.String(required=True)
        run_id = marsh.fields.UUID(required=True)

        def _make(self, data: dict) -> "LogEntry":
            return LogEntry(**data)

    timestamp = DateTimeField(null=False)
    message = CharField(null=False)
    run_id = ForeignKeyField(Run, null=False)


class TrainSpawnLogEntry(LogEntry):
    """A LogEntry that represents the spawning of a train."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainSpawnLogEntry model."""

        train_id = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrainSpawnLogEntry":
            return TrainSpawnLogEntry(**data)

    train_id = IntegerField(null=False)


class TrainRemoveLogEntry(LogEntry):
    """A LogEntry that represents the removal of a train."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainRemoveLogEntry model."""

        train_id = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrainRemoveLogEntry":
            return TrainRemoveLogEntry(**data)

    train_id = IntegerField(null=False)


class TrainArrivalLogEntry(LogEntry):
    """A LogEntry that represents the arrival of a train at a station."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainArrivalLogEntry model."""

        train_id = marsh.fields.Integer(required=True)
        station_id = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrainArrivalLogEntry":
            return TrainArrivalLogEntry(**data)

    train_id = IntegerField(null=False)
    station_id = IntegerField(null=False)


class TrainDepartureLogEntry(LogEntry):
    """A LogEntry that represents the departure of a train from a station."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the TrainDepartureLogEntry model."""

        train_id = marsh.fields.Integer(required=True)
        station_id = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrainDepartureLogEntry":
            return TrainDepartureLogEntry(**data)

    train_id = IntegerField(null=False)
    station_id = IntegerField(null=False)


class CreateFahrstrasseLogEntry(LogEntry):
    """A LogEntry that represents the creation of a fahrstrasse."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the CreateFahrstrasseLogEntry model."""

        fahrstrasse = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "CreateFahrstrasseLogEntry":
            return CreateFahrstrasseLogEntry(**data)

    fahrstrasse = CharField(null=False)


class RemoveFahrstrasseLogEntry(LogEntry):
    """A LogEntry that represents the removal of a fahrstrasse."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the RemoveFahrstrasseLogEntry model."""

        fahrstrasse = marsh.fields.String(required=True)

        def _make(self, data: dict) -> "RemoveFahrstrasseLogEntry":
            return RemoveFahrstrasseLogEntry(**data)

    fahrstrasse = CharField(null=False)


class SetSignalLogEntry(LogEntry):
    """A LogEntry that represents the setting of a signal."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the SetSignalLogEntry model."""

        signal_id = marsh.fields.String(required=True)
        state_before = marsh.fields.Integer(required=True)
        state_after = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "SetSignalLogEntry":
            return SetSignalLogEntry(**data)

    signal_id = CharField(null=False)
    state_before = IntegerField(null=False)
    state_after = IntegerField(null=False)


class InjectFaultLogEntry(LogEntry):
    """A LogEntry that represents the injection of a fault."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the InjectFaultLogEntry model."""

        injection_id = marsh.fields.Integer(required=True)
        fault_type = marsh.fields.Integer(required=True)
        injection_position = marsh.fields.String(required=True)
        duration = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "InjectFaultLogEntry":
            return InjectFaultLogEntry(**data)

    injection_id = IntegerField(null=False)
    fault_type = IntegerField(null=False)
    injection_position = CharField(null=False)
    duration = IntegerField(null=False)


class RemoveFaultLogEntry(LogEntry):
    """A LogEntry that represents the removal of a fault."""

    class Schema(LogEntry.Schema):
        """The marshmallow schema for the RemoveFaultLogEntry model."""

        injection_id = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "InjectFaultLogEntry":
            return RemoveFaultLogEntry(**data)

    injection_id = IntegerField(null=False)
