# pylint: disable=too-many-lines
from datetime import datetime
from uuid import UUID

import pytest
from marshmallow import ValidationError
from peewee import IntegrityError

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
from tests.decorators import recreate_db_setup


class TestLogEntry:
    """Class for testing all LogEntry classes."""

    class TestLogEntry:
        """Test LogEntry."""

        @pytest.fixture
        def log_entry_as_dict(self, timestamp, tick, message, run):
            """LogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
            }

        @pytest.fixture
        def log_entry_as_dict_serialized(self, timestamp, tick, message, run):
            """LogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
            }

        @pytest.fixture
        def empty_log_entry_as_dict(self):
            """LogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, log_entry_as_dict):
            """Test that Log Entry can be created."""
            log_entry = LogEntry.create(**log_entry_as_dict)
            assert (
                LogEntry.select().where(LogEntry.id == log_entry.id).first()
                == log_entry
            )

        def test_create_empty_fails(self, empty_log_entry_as_dict):
            """Test that Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                LogEntry.create(**empty_log_entry_as_dict)

        def test_serialization(self, log_entry_as_dict):
            """Test that Log Entry can be serialized."""
            log_entry = LogEntry.create(**log_entry_as_dict)
            assert log_entry.timestamp == log_entry_as_dict["timestamp"]
            assert log_entry.tick == log_entry_as_dict["tick"]
            assert log_entry.message == log_entry_as_dict["message"]
            assert log_entry.run_id.id == log_entry_as_dict["run_id"]

            assert log_entry.to_dict() == {
                "id": str(log_entry.id),
                # pylint: disable=no-member
                "created_at": log_entry.created_at.isoformat(),
                "updated_at": log_entry.updated_at.isoformat(),
                "timestamp": log_entry_as_dict["timestamp"].isoformat(),
                "tick": log_entry_as_dict["tick"],
                "message": log_entry_as_dict["message"],
                "run_id": str(log_entry_as_dict["run_id"]),
            }

        def test_deserialization(self, log_entry_as_dict_serialized):
            """Test that Log Entry can be deserialized."""
            log_entry = LogEntry.Schema().load(log_entry_as_dict_serialized)
            assert isinstance(log_entry, LogEntry)
            assert isinstance(log_entry.id, UUID)
            assert isinstance(log_entry.timestamp, datetime)
            assert isinstance(log_entry.tick, int)
            assert isinstance(log_entry.message, str)
            assert isinstance(log_entry.run_id, Run)
            assert (
                log_entry.timestamp.isoformat()
                == log_entry_as_dict_serialized["timestamp"]
            )
            assert log_entry.tick == log_entry_as_dict_serialized["tick"]
            assert log_entry.message == log_entry_as_dict_serialized["message"]
            assert str(log_entry.run_id) == log_entry_as_dict_serialized["run_id"]

        def test_deserialization_empty_fails(self, empty_log_entry_as_dict):
            """Test that Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                LogEntry.Schema().load(empty_log_entry_as_dict)

    class TestTrainSpawnLogEntry:
        """Tests for TrainSpawnLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_spawn_log_entry_as_dict(
            self, timestamp, tick, message, run, train_id
        ):
            """TrainSpawnLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_spawn_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, train_id
        ):
            """TrainSpawnLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_id": train_id,
            }

        @pytest.fixture
        def empty_train_spawn_log_entry_as_dict(self):
            """TrainSpawnLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, train_spawn_log_entry_as_dict):
            """Test that Train Spawn Log Entry can be created."""
            train_spawn_log_entry = TrainSpawnLogEntry.create(
                **train_spawn_log_entry_as_dict
            )
            assert (
                TrainSpawnLogEntry.select()
                .where(TrainSpawnLogEntry.id == train_spawn_log_entry.id)
                .first()
                == train_spawn_log_entry
            )

        def test_create_empty_fails(self, empty_train_spawn_log_entry_as_dict):
            """Test that Train Spawn Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                TrainSpawnLogEntry.create(**empty_train_spawn_log_entry_as_dict)

        def test_serialization(self, train_spawn_log_entry_as_dict):
            """Test that Train Spawn Log Entry can be serialized."""
            train_spawn_log_entry = TrainSpawnLogEntry.create(
                **train_spawn_log_entry_as_dict
            )
            assert (
                train_spawn_log_entry.timestamp
                == train_spawn_log_entry_as_dict["timestamp"]
            )
            assert train_spawn_log_entry.tick == train_spawn_log_entry_as_dict["tick"]
            assert (
                train_spawn_log_entry.message
                == train_spawn_log_entry_as_dict["message"]
            )
            assert (
                train_spawn_log_entry.run_id.id
                == train_spawn_log_entry_as_dict["run_id"]
            )
            assert (
                train_spawn_log_entry.train_id
                == train_spawn_log_entry_as_dict["train_id"]
            )

            assert train_spawn_log_entry.to_dict() == {
                "id": str(train_spawn_log_entry.id),
                # pylint: disable=no-member
                "created_at": train_spawn_log_entry.created_at.isoformat(),
                "updated_at": train_spawn_log_entry.updated_at.isoformat(),
                "timestamp": train_spawn_log_entry_as_dict["timestamp"].isoformat(),
                "tick": train_spawn_log_entry_as_dict["tick"],
                "message": train_spawn_log_entry_as_dict["message"],
                "run_id": str(train_spawn_log_entry_as_dict["run_id"]),
                "train_id": train_spawn_log_entry_as_dict["train_id"],
            }

        def test_deserialization(self, train_spawn_log_entry_as_dict_serialized):
            """Test that Train Spawn Log Entry can be deserialized."""
            train_spawn_log_entry = TrainSpawnLogEntry.Schema().load(
                train_spawn_log_entry_as_dict_serialized
            )
            assert isinstance(train_spawn_log_entry, TrainSpawnLogEntry)
            assert isinstance(train_spawn_log_entry.id, UUID)
            assert isinstance(train_spawn_log_entry.timestamp, datetime)
            assert isinstance(train_spawn_log_entry.tick, int)
            assert isinstance(train_spawn_log_entry.message, str)
            assert isinstance(train_spawn_log_entry.run_id, Run)
            assert isinstance(train_spawn_log_entry.train_id, str)
            assert (
                train_spawn_log_entry.timestamp.isoformat()
                == train_spawn_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                train_spawn_log_entry.tick
                == train_spawn_log_entry_as_dict_serialized["tick"]
            )
            assert (
                train_spawn_log_entry.message
                == train_spawn_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(train_spawn_log_entry.run_id)
                == train_spawn_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                train_spawn_log_entry.train_id
                == train_spawn_log_entry_as_dict_serialized["train_id"]
            )

        def test_deserialization_empty_fails(self, empty_train_spawn_log_entry_as_dict):
            """Test that Train Spawn Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                TrainSpawnLogEntry.Schema().load(empty_train_spawn_log_entry_as_dict)

    class TestTrainRemoveLogEntry:
        """Tests for TrainRemoveLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_remove_log_entry_as_dict(
            self, timestamp, tick, message, run, train_id
        ):
            """TrainRemoveLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_remove_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, train_id
        ):
            """TrainRemoveLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_id": train_id,
            }

        @pytest.fixture
        def empty_train_remove_log_entry_as_dict(self):
            """TrainRemoveLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, train_remove_log_entry_as_dict):
            """Test that Train Remove Log Entry can be created."""
            train_remove_log_entry = TrainRemoveLogEntry.create(
                **train_remove_log_entry_as_dict
            )
            assert (
                TrainRemoveLogEntry.select()
                .where(TrainRemoveLogEntry.id == train_remove_log_entry.id)
                .first()
                == train_remove_log_entry
            )

        def test_create_empty_fails(self, empty_train_remove_log_entry_as_dict):
            """Test that Train Remove Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                TrainRemoveLogEntry.create(**empty_train_remove_log_entry_as_dict)

        def test_serialization(self, train_remove_log_entry_as_dict):
            """Test that Train Remove Log Entry can be serialized."""
            train_remove_log_entry = TrainRemoveLogEntry.create(
                **train_remove_log_entry_as_dict
            )
            assert (
                train_remove_log_entry.timestamp
                == train_remove_log_entry_as_dict["timestamp"]
            )
            assert train_remove_log_entry.tick == train_remove_log_entry_as_dict["tick"]
            assert (
                train_remove_log_entry.message
                == train_remove_log_entry_as_dict["message"]
            )
            assert (
                train_remove_log_entry.run_id.id
                == train_remove_log_entry_as_dict["run_id"]
            )
            assert (
                train_remove_log_entry.train_id
                == train_remove_log_entry_as_dict["train_id"]
            )

            assert train_remove_log_entry.to_dict() == {
                "id": str(train_remove_log_entry.id),
                # pylint: disable=no-member
                "created_at": train_remove_log_entry.created_at.isoformat(),
                "updated_at": train_remove_log_entry.updated_at.isoformat(),
                "timestamp": train_remove_log_entry_as_dict["timestamp"].isoformat(),
                "tick": train_remove_log_entry_as_dict["tick"],
                "message": train_remove_log_entry_as_dict["message"],
                "run_id": str(train_remove_log_entry_as_dict["run_id"]),
                "train_id": train_remove_log_entry_as_dict["train_id"],
            }

        def test_deserialization(self, train_remove_log_entry_as_dict_serialized):
            """Test that Train Remove Log Entry can be deserialized."""
            train_remove_log_entry = TrainRemoveLogEntry.Schema().load(
                train_remove_log_entry_as_dict_serialized
            )
            assert isinstance(train_remove_log_entry, TrainRemoveLogEntry)
            assert isinstance(train_remove_log_entry.id, UUID)
            assert isinstance(train_remove_log_entry.timestamp, datetime)
            assert isinstance(train_remove_log_entry.tick, int)
            assert isinstance(train_remove_log_entry.message, str)
            assert isinstance(train_remove_log_entry.run_id, Run)
            assert isinstance(train_remove_log_entry.train_id, str)
            assert (
                train_remove_log_entry.timestamp.isoformat()
                == train_remove_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                train_remove_log_entry.tick
                == train_remove_log_entry_as_dict_serialized["tick"]
            )
            assert (
                train_remove_log_entry.message
                == train_remove_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(train_remove_log_entry.run_id)
                == train_remove_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                train_remove_log_entry.train_id
                == train_remove_log_entry_as_dict_serialized["train_id"]
            )

    class TestTrainArrivalLogEntry:
        """Tests for TrainArrivalLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_arrival_log_entry_as_dict(
            self, timestamp, tick, message, run, train_id, station_id
        ):
            """TrainArrivalLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
                "station_id": station_id,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_arrival_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, train_id, station_id
        ):
            """TrainArrivalLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_id": train_id,
                "station_id": station_id,
            }

        @pytest.fixture
        def empty_train_arrival_log_entry_as_dict(self):
            """TrainArrivalLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, train_arrival_log_entry_as_dict):
            """Test that Train Arrival Log Entry can be created."""
            train_arrival_log_entry = TrainArrivalLogEntry.create(
                **train_arrival_log_entry_as_dict
            )
            assert (
                TrainArrivalLogEntry.select()
                .where(TrainArrivalLogEntry.id == train_arrival_log_entry.id)
                .first()
                == train_arrival_log_entry
            )

        def test_create_empty_fails(self, empty_train_arrival_log_entry_as_dict):
            """Test that Train Arrival Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                TrainArrivalLogEntry.create(**empty_train_arrival_log_entry_as_dict)

        def test_serialization(self, train_arrival_log_entry_as_dict):
            """Test that Train Arrival Log Entry can be serialized."""
            train_arrival_log_entry = TrainArrivalLogEntry.create(
                **train_arrival_log_entry_as_dict
            )
            assert (
                train_arrival_log_entry.timestamp
                == train_arrival_log_entry_as_dict["timestamp"]
            )
            assert (
                train_arrival_log_entry.tick == train_arrival_log_entry_as_dict["tick"]
            )
            assert (
                train_arrival_log_entry.message
                == train_arrival_log_entry_as_dict["message"]
            )
            assert (
                train_arrival_log_entry.run_id.id
                == train_arrival_log_entry_as_dict["run_id"]
            )
            assert (
                train_arrival_log_entry.train_id
                == train_arrival_log_entry_as_dict["train_id"]
            )
            assert (
                train_arrival_log_entry.station_id
                == train_arrival_log_entry_as_dict["station_id"]
            )

            assert train_arrival_log_entry.to_dict() == {
                "id": str(train_arrival_log_entry.id),
                # pylint: disable=no-member
                "created_at": train_arrival_log_entry.created_at.isoformat(),
                "updated_at": train_arrival_log_entry.updated_at.isoformat(),
                "timestamp": train_arrival_log_entry_as_dict["timestamp"].isoformat(),
                "tick": train_arrival_log_entry_as_dict["tick"],
                "message": train_arrival_log_entry_as_dict["message"],
                "run_id": str(train_arrival_log_entry_as_dict["run_id"]),
                "train_id": train_arrival_log_entry_as_dict["train_id"],
                "station_id": train_arrival_log_entry_as_dict["station_id"],
            }

        def test_deserialization(self, train_arrival_log_entry_as_dict_serialized):
            """Test that Train Arrival Log Entry can be deserialized."""
            train_arrival_log_entry = TrainArrivalLogEntry.Schema().load(
                train_arrival_log_entry_as_dict_serialized
            )
            assert isinstance(train_arrival_log_entry, TrainArrivalLogEntry)
            assert isinstance(train_arrival_log_entry.id, UUID)
            assert isinstance(train_arrival_log_entry.timestamp, datetime)
            assert isinstance(train_arrival_log_entry.tick, int)
            assert isinstance(train_arrival_log_entry.message, str)
            assert isinstance(train_arrival_log_entry.run_id, Run)
            assert isinstance(train_arrival_log_entry.train_id, str)
            assert isinstance(train_arrival_log_entry.station_id, str)
            assert (
                train_arrival_log_entry.timestamp.isoformat()
                == train_arrival_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                train_arrival_log_entry.tick
                == train_arrival_log_entry_as_dict_serialized["tick"]
            )
            assert (
                train_arrival_log_entry.message
                == train_arrival_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(train_arrival_log_entry.run_id)
                == train_arrival_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                train_arrival_log_entry.train_id
                == train_arrival_log_entry_as_dict_serialized["train_id"]
            )
            assert (
                train_arrival_log_entry.station_id
                == train_arrival_log_entry_as_dict_serialized["station_id"]
            )

        def test_deserialization_empty_fails(
            self, empty_train_arrival_log_entry_as_dict
        ):
            """Test that Train Arrival Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                TrainArrivalLogEntry.Schema().load(
                    empty_train_arrival_log_entry_as_dict
                )

    class TestTrainDepartureLogEntry:
        """Tests for the Train Departure Log Entry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_departure_log_entry_as_dict(
            self, timestamp, tick, message, run, train_id, station_id
        ):
            """TrainDepartureLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
                "station_id": station_id,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def train_departure_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, train_id, station_id
        ):
            """TrainDepartureLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_id": train_id,
                "station_id": station_id,
            }

        @pytest.fixture
        def empty_train_departure_log_entry_as_dict(self):
            """TrainDepartureLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, train_departure_log_entry_as_dict):
            """Test that Train Departure Log Entry can be created."""
            train_departure_log_entry = TrainDepartureLogEntry.create(
                **train_departure_log_entry_as_dict
            )
            assert (
                TrainDepartureLogEntry.select()
                .where(TrainDepartureLogEntry.id == train_departure_log_entry.id)
                .first()
                == train_departure_log_entry
            )

        def test_create_empty_fails(self, empty_train_departure_log_entry_as_dict):
            """Test that Train Departure Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                TrainDepartureLogEntry.create(**empty_train_departure_log_entry_as_dict)

        def test_serialization(self, train_departure_log_entry_as_dict):
            """Test that Train Departure Log Entry can be serialized."""
            train_departure_log_entry = TrainDepartureLogEntry.create(
                **train_departure_log_entry_as_dict
            )
            assert (
                train_departure_log_entry.timestamp
                == train_departure_log_entry_as_dict["timestamp"]
            )
            assert (
                train_departure_log_entry.tick
                == train_departure_log_entry_as_dict["tick"]
            )
            assert (
                train_departure_log_entry.message
                == train_departure_log_entry_as_dict["message"]
            )
            assert (
                train_departure_log_entry.run_id.id
                == train_departure_log_entry_as_dict["run_id"]
            )
            assert (
                train_departure_log_entry.train_id
                == train_departure_log_entry_as_dict["train_id"]
            )
            assert (
                train_departure_log_entry.station_id
                == train_departure_log_entry_as_dict["station_id"]
            )

            assert train_departure_log_entry.to_dict() == {
                "id": str(train_departure_log_entry.id),
                # pylint: disable=no-member
                "created_at": train_departure_log_entry.created_at.isoformat(),
                "updated_at": train_departure_log_entry.updated_at.isoformat(),
                "timestamp": train_departure_log_entry_as_dict["timestamp"].isoformat(),
                "tick": train_departure_log_entry_as_dict["tick"],
                "message": train_departure_log_entry_as_dict["message"],
                "run_id": str(train_departure_log_entry_as_dict["run_id"]),
                "train_id": train_departure_log_entry_as_dict["train_id"],
                "station_id": train_departure_log_entry_as_dict["station_id"],
            }

        def test_deserialization(self, train_departure_log_entry_as_dict_serialized):
            """Test that Train Departure Log Entry can be deserialized."""
            train_departure_log_entry = TrainDepartureLogEntry.Schema().load(
                train_departure_log_entry_as_dict_serialized
            )
            assert isinstance(train_departure_log_entry, TrainDepartureLogEntry)
            assert isinstance(train_departure_log_entry.id, UUID)
            assert isinstance(train_departure_log_entry.timestamp, datetime)
            assert isinstance(train_departure_log_entry.tick, int)
            assert isinstance(train_departure_log_entry.message, str)
            assert isinstance(train_departure_log_entry.run_id, Run)
            assert isinstance(train_departure_log_entry.train_id, str)
            assert isinstance(train_departure_log_entry.station_id, str)
            assert (
                train_departure_log_entry.timestamp.isoformat()
                == train_departure_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                train_departure_log_entry.tick
                == train_departure_log_entry_as_dict_serialized["tick"]
            )
            assert (
                train_departure_log_entry.message
                == train_departure_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(train_departure_log_entry.run_id)
                == train_departure_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                train_departure_log_entry.train_id
                == train_departure_log_entry_as_dict_serialized["train_id"]
            )
            assert (
                train_departure_log_entry.station_id
                == train_departure_log_entry_as_dict_serialized["station_id"]
            )

        def test_deserialization_empty_fails(
            self, empty_train_departure_log_entry_as_dict
        ):
            """Test that Train Departure Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                TrainDepartureLogEntry.Schema().load(
                    empty_train_departure_log_entry_as_dict
                )

    class TestCreateFahrstrasseLogEntry:
        """Tests for CreateFahrstrasseLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def create_fahrstrasse_log_entry_as_dict(
            self, timestamp, tick, message, run, fahrstrasse
        ):
            """CreateFahrstrasseLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "fahrstrasse": fahrstrasse,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def create_fahrstrasse_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, fahrstrasse
        ):
            """CreateFahrstrasseLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "fahrstrasse": fahrstrasse,
            }

        @pytest.fixture
        def empty_create_fahrstrasse_log_entry_as_dict(self):
            """CreateFahrstrasseLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, create_fahrstrasse_log_entry_as_dict):
            """Test that Create Fahrstrasse Log Entry can be created."""
            create_fahrstrasse_log_entry = CreateFahrstrasseLogEntry.create(
                **create_fahrstrasse_log_entry_as_dict
            )
            assert (
                CreateFahrstrasseLogEntry.select()
                .where(CreateFahrstrasseLogEntry.id == create_fahrstrasse_log_entry.id)
                .first()
                == create_fahrstrasse_log_entry
            )

        def test_create_empty_fails(self, empty_create_fahrstrasse_log_entry_as_dict):
            """Test that Create Fahrstrasse Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                CreateFahrstrasseLogEntry.create(
                    **empty_create_fahrstrasse_log_entry_as_dict
                )

        def test_serialization(self, create_fahrstrasse_log_entry_as_dict):
            """Test that Create Fahrstrasse Log Entry can be serialized."""
            create_fahrstrasse_log_entry = CreateFahrstrasseLogEntry.create(
                **create_fahrstrasse_log_entry_as_dict
            )
            assert (
                create_fahrstrasse_log_entry.timestamp
                == create_fahrstrasse_log_entry_as_dict["timestamp"]
            )
            assert (
                create_fahrstrasse_log_entry.tick
                == create_fahrstrasse_log_entry_as_dict["tick"]
            )
            assert (
                create_fahrstrasse_log_entry.message
                == create_fahrstrasse_log_entry_as_dict["message"]
            )
            assert (
                create_fahrstrasse_log_entry.run_id.id
                == create_fahrstrasse_log_entry_as_dict["run_id"]
            )
            assert (
                create_fahrstrasse_log_entry.fahrstrasse
                == create_fahrstrasse_log_entry_as_dict["fahrstrasse"]
            )

            assert create_fahrstrasse_log_entry.to_dict() == {
                "id": str(create_fahrstrasse_log_entry.id),
                # pylint: disable=no-member
                "created_at": create_fahrstrasse_log_entry.created_at.isoformat(),
                "updated_at": create_fahrstrasse_log_entry.updated_at.isoformat(),
                "timestamp": create_fahrstrasse_log_entry_as_dict[
                    "timestamp"
                ].isoformat(),
                "tick": create_fahrstrasse_log_entry_as_dict["tick"],
                "message": create_fahrstrasse_log_entry_as_dict["message"],
                "run_id": str(create_fahrstrasse_log_entry_as_dict["run_id"]),
                "fahrstrasse": create_fahrstrasse_log_entry_as_dict["fahrstrasse"],
            }

        def test_deserialization(self, create_fahrstrasse_log_entry_as_dict_serialized):
            """Test that Create Fahrstrasse Log Entry can be deserialized."""
            create_fahrstrasse_log_entry = CreateFahrstrasseLogEntry.Schema().load(
                create_fahrstrasse_log_entry_as_dict_serialized
            )
            assert isinstance(create_fahrstrasse_log_entry, CreateFahrstrasseLogEntry)
            assert isinstance(create_fahrstrasse_log_entry.id, UUID)
            assert isinstance(create_fahrstrasse_log_entry.timestamp, datetime)
            assert isinstance(create_fahrstrasse_log_entry.tick, int)
            assert isinstance(create_fahrstrasse_log_entry.message, str)
            assert isinstance(create_fahrstrasse_log_entry.run_id, Run)
            assert isinstance(create_fahrstrasse_log_entry.fahrstrasse, str)
            assert (
                create_fahrstrasse_log_entry.timestamp.isoformat()
                == create_fahrstrasse_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                create_fahrstrasse_log_entry.tick
                == create_fahrstrasse_log_entry_as_dict_serialized["tick"]
            )
            assert (
                create_fahrstrasse_log_entry.message
                == create_fahrstrasse_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(create_fahrstrasse_log_entry.run_id)
                == create_fahrstrasse_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                create_fahrstrasse_log_entry.fahrstrasse
                == create_fahrstrasse_log_entry_as_dict_serialized["fahrstrasse"]
            )

        def test_deserialization_empty_fails(
            self, empty_create_fahrstrasse_log_entry_as_dict
        ):
            """Test that Create Fahrstrasse Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                CreateFahrstrasseLogEntry.Schema().load(
                    empty_create_fahrstrasse_log_entry_as_dict
                )

    class TestRemoveFahrstrasseLogEntry:
        """Tests for RemoveFahrstrasseLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def remove_fahrstrasse_log_entry_as_dict(
            self, timestamp, tick, message, run, fahrstrasse
        ):
            """RemoveFahrstrasseLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "fahrstrasse": fahrstrasse,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def remove_fahrstrasse_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, fahrstrasse
        ):
            """RemoveFahrstrasseLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "fahrstrasse": fahrstrasse,
            }

        @pytest.fixture
        def empty_remove_fahrstrasse_log_entry_as_dict(self):
            """RemoveFahrstrasseLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, remove_fahrstrasse_log_entry_as_dict):
            """Test that Remove Fahrstrasse Log Entry can be created."""
            remove_fahrstrasse_log_entry = RemoveFahrstrasseLogEntry.create(
                **remove_fahrstrasse_log_entry_as_dict
            )
            assert (
                RemoveFahrstrasseLogEntry.select()
                .where(RemoveFahrstrasseLogEntry.id == remove_fahrstrasse_log_entry.id)
                .first()
                == remove_fahrstrasse_log_entry
            )

        def test_create_empty_fails(self, empty_remove_fahrstrasse_log_entry_as_dict):
            """Test that Remove Fahrstrasse Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                RemoveFahrstrasseLogEntry.create(
                    **empty_remove_fahrstrasse_log_entry_as_dict
                )

        def test_serialization(self, remove_fahrstrasse_log_entry_as_dict):
            """Test that Remove Fahrstrasse Log Entry can be serialized."""
            remove_fahrstrasse_log_entry = RemoveFahrstrasseLogEntry.create(
                **remove_fahrstrasse_log_entry_as_dict
            )
            assert (
                remove_fahrstrasse_log_entry.timestamp
                == remove_fahrstrasse_log_entry_as_dict["timestamp"]
            )
            assert (
                remove_fahrstrasse_log_entry.tick
                == remove_fahrstrasse_log_entry_as_dict["tick"]
            )
            assert (
                remove_fahrstrasse_log_entry.message
                == remove_fahrstrasse_log_entry_as_dict["message"]
            )
            assert (
                remove_fahrstrasse_log_entry.run_id.id
                == remove_fahrstrasse_log_entry_as_dict["run_id"]
            )
            assert (
                remove_fahrstrasse_log_entry.fahrstrasse
                == remove_fahrstrasse_log_entry_as_dict["fahrstrasse"]
            )

            assert remove_fahrstrasse_log_entry.to_dict() == {
                "id": str(remove_fahrstrasse_log_entry.id),
                # pylint: disable=no-member
                "created_at": remove_fahrstrasse_log_entry.created_at.isoformat(),
                "updated_at": remove_fahrstrasse_log_entry.updated_at.isoformat(),
                "timestamp": remove_fahrstrasse_log_entry_as_dict[
                    "timestamp"
                ].isoformat(),
                "tick": remove_fahrstrasse_log_entry_as_dict["tick"],
                "message": remove_fahrstrasse_log_entry_as_dict["message"],
                "run_id": str(remove_fahrstrasse_log_entry_as_dict["run_id"]),
                "fahrstrasse": remove_fahrstrasse_log_entry_as_dict["fahrstrasse"],
            }

        def test_deserialization(self, remove_fahrstrasse_log_entry_as_dict_serialized):
            """Test that Remove Fahrstrasse Log Entry can be deserialized."""
            remove_fahrstrasse_log_entry = RemoveFahrstrasseLogEntry.Schema().load(
                remove_fahrstrasse_log_entry_as_dict_serialized
            )
            assert isinstance(remove_fahrstrasse_log_entry, RemoveFahrstrasseLogEntry)
            assert isinstance(remove_fahrstrasse_log_entry.id, UUID)
            assert isinstance(remove_fahrstrasse_log_entry.timestamp, datetime)
            assert isinstance(remove_fahrstrasse_log_entry.tick, int)
            assert isinstance(remove_fahrstrasse_log_entry.message, str)
            assert isinstance(remove_fahrstrasse_log_entry.run_id, Run)
            assert isinstance(remove_fahrstrasse_log_entry.fahrstrasse, str)
            assert (
                remove_fahrstrasse_log_entry.timestamp.isoformat()
                == remove_fahrstrasse_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                remove_fahrstrasse_log_entry.tick
                == remove_fahrstrasse_log_entry_as_dict_serialized["tick"]
            )
            assert (
                remove_fahrstrasse_log_entry.message
                == remove_fahrstrasse_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(remove_fahrstrasse_log_entry.run_id)
                == remove_fahrstrasse_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                remove_fahrstrasse_log_entry.fahrstrasse
                == remove_fahrstrasse_log_entry_as_dict_serialized["fahrstrasse"]
            )

        def test_deserialization_empty_fails(
            self, empty_remove_fahrstrasse_log_entry_as_dict
        ):
            """Test that Remove Fahrstrasse Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                RemoveFahrstrasseLogEntry.Schema().load(
                    empty_remove_fahrstrasse_log_entry_as_dict
                )

    class TestSignalLogEntry:
        """Tests for SignalLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def set_signal_log_entry_as_dict(
            self, timestamp, tick, message, run, signal_id, state_before, state_after
        ):
            """SetSignalLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "signal_id": signal_id,
                "state_before": state_before,
                "state_after": state_after,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def set_signal_log_entry_as_dict_serialized(
            self, timestamp, tick, message, run, signal_id, state_before, state_after
        ):
            """SetSignalLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "signal_id": str(signal_id),
                "state_before": state_before,
                "state_after": state_after,
            }

        @pytest.fixture
        def empty_set_signal_log_entry_as_dict(self):
            """SetSignalLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, set_signal_log_entry_as_dict):
            """Test that Set Signal Log Entry can be created."""
            set_signal_log_entry = SetSignalLogEntry.create(
                **set_signal_log_entry_as_dict
            )
            assert (
                SetSignalLogEntry.select()
                .where(SetSignalLogEntry.id == set_signal_log_entry.id)
                .first()
                == set_signal_log_entry
            )

        def test_create_empty_fails(self, empty_set_signal_log_entry_as_dict):
            """Test that Set Signal Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                SetSignalLogEntry.create(**empty_set_signal_log_entry_as_dict)

        def test_serialization(self, set_signal_log_entry_as_dict):
            """Test that Set Signal Log Entry can be serialized."""
            set_signal_log_entry = SetSignalLogEntry.create(
                **set_signal_log_entry_as_dict
            )
            assert (
                set_signal_log_entry.timestamp
                == set_signal_log_entry_as_dict["timestamp"]
            )
            assert set_signal_log_entry.tick == set_signal_log_entry_as_dict["tick"]
            assert (
                set_signal_log_entry.message == set_signal_log_entry_as_dict["message"]
            )
            assert (
                set_signal_log_entry.run_id.id == set_signal_log_entry_as_dict["run_id"]
            )
            assert (
                set_signal_log_entry.signal_id
                == set_signal_log_entry_as_dict["signal_id"]
            )
            assert (
                set_signal_log_entry.state_before
                == set_signal_log_entry_as_dict["state_before"]
            )
            assert (
                set_signal_log_entry.state_after
                == set_signal_log_entry_as_dict["state_after"]
            )

            assert set_signal_log_entry.to_dict() == {
                "id": str(set_signal_log_entry.id),
                # pylint: disable=no-member
                "created_at": set_signal_log_entry.created_at.isoformat(),
                "updated_at": set_signal_log_entry.updated_at.isoformat(),
                "timestamp": set_signal_log_entry_as_dict["timestamp"].isoformat(),
                "tick": set_signal_log_entry_as_dict["tick"],
                "message": set_signal_log_entry_as_dict["message"],
                "run_id": str(set_signal_log_entry_as_dict["run_id"]),
                "signal_id": str(set_signal_log_entry_as_dict["signal_id"]),
                "state_before": set_signal_log_entry_as_dict["state_before"],
                "state_after": set_signal_log_entry_as_dict["state_after"],
            }

        def test_deserialization(self, set_signal_log_entry_as_dict_serialized):
            """Test that Set Signal Log Entry can be deserialized."""
            set_signal_log_entry = SetSignalLogEntry.Schema().load(
                set_signal_log_entry_as_dict_serialized
            )
            assert isinstance(set_signal_log_entry, SetSignalLogEntry)
            assert isinstance(set_signal_log_entry.id, UUID)
            assert isinstance(set_signal_log_entry.timestamp, datetime)
            assert isinstance(set_signal_log_entry.tick, int)
            assert isinstance(set_signal_log_entry.message, str)
            assert isinstance(set_signal_log_entry.run_id, Run)
            assert isinstance(set_signal_log_entry.signal_id, UUID)
            assert isinstance(set_signal_log_entry.state_before, int)
            assert isinstance(set_signal_log_entry.state_after, int)
            assert (
                set_signal_log_entry.timestamp.isoformat()
                == set_signal_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                set_signal_log_entry.tick
                == set_signal_log_entry_as_dict_serialized["tick"]
            )
            assert (
                set_signal_log_entry.message
                == set_signal_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(set_signal_log_entry.run_id)
                == set_signal_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                str(set_signal_log_entry.signal_id)
                == set_signal_log_entry_as_dict_serialized["signal_id"]
            )
            assert (
                set_signal_log_entry.state_before
                == set_signal_log_entry_as_dict_serialized["state_before"]
            )
            assert (
                set_signal_log_entry.state_after
                == set_signal_log_entry_as_dict_serialized["state_after"]
            )

        def test_deserialization_empty_fails(self, empty_set_signal_log_entry_as_dict):
            """Test that Set Signal Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                SetSignalLogEntry.Schema().load(empty_set_signal_log_entry_as_dict)

    class TestInjectFaultLogEntry:
        """Tests for InjectFaultLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def inject_fault_log_entry_as_dict(
            self,
            timestamp,
            tick,
            message,
            run,
            train_speed_fault_configuration,
            platform_blocked_fault_configuration,
            train_cancelled_fault_configuration,
            affected_element,
            value_before,
            value_after,
        ):
            """InjectFaultLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_speed_fault_configuration": train_speed_fault_configuration.id,
                "platform_blocked_fault_configuration": platform_blocked_fault_configuration.id,
                "train_cancelled_fault_configuration": train_cancelled_fault_configuration.id,
                "affected_element": affected_element,
                "value_before": value_before,
                "value_after": value_after,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def inject_fault_log_entry_as_dict_serialized(
            self,
            timestamp,
            tick,
            message,
            run,
            train_speed_fault_configuration,
            platform_blocked_fault_configuration,
            train_cancelled_fault_configuration,
            affected_element,
            value_before,
            value_after,
        ):
            """InjectFaultLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_speed_fault_configuration": str(
                    train_speed_fault_configuration.id
                ),
                "platform_blocked_fault_configuration": str(
                    platform_blocked_fault_configuration.id
                ),
                "train_cancelled_fault_configuration": str(
                    train_cancelled_fault_configuration.id
                ),
                "affected_element": affected_element,
                "value_before": value_before,
                "value_after": value_after,
            }

        @pytest.fixture
        def empty_inject_fault_log_entry_as_dict(self):
            """InjectFaultLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, inject_fault_log_entry_as_dict):
            """Test that Inject Fault Log Entry can be created."""
            inject_fault_log_entry = InjectFaultLogEntry.create(
                **inject_fault_log_entry_as_dict
            )
            assert (
                InjectFaultLogEntry.select()
                .where(InjectFaultLogEntry.id == inject_fault_log_entry.id)
                .first()
                == inject_fault_log_entry
            )

        def test_create_empty_fails(self, empty_inject_fault_log_entry_as_dict):
            """Test that Inject Fault Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                InjectFaultLogEntry.create(**empty_inject_fault_log_entry_as_dict)

        def test_serialization(self, inject_fault_log_entry_as_dict):
            """Test that Inject Fault Log Entry can be serialized."""
            inject_fault_log_entry = InjectFaultLogEntry.create(
                **inject_fault_log_entry_as_dict
            )
            assert (
                inject_fault_log_entry.timestamp
                == inject_fault_log_entry_as_dict["timestamp"]
            )
            assert inject_fault_log_entry.tick == inject_fault_log_entry_as_dict["tick"]
            assert (
                inject_fault_log_entry.message
                == inject_fault_log_entry_as_dict["message"]
            )
            assert (
                inject_fault_log_entry.run_id.id
                == inject_fault_log_entry_as_dict["run_id"]
            )
            assert (
                inject_fault_log_entry.train_speed_fault_configuration.id
                == inject_fault_log_entry_as_dict["train_speed_fault_configuration"]
            )
            assert (
                inject_fault_log_entry.platform_blocked_fault_configuration.id
                == inject_fault_log_entry_as_dict[
                    "platform_blocked_fault_configuration"
                ]
            )
            assert (
                inject_fault_log_entry.train_cancelled_fault_configuration.id
                == inject_fault_log_entry_as_dict["train_cancelled_fault_configuration"]
            )
            assert (
                inject_fault_log_entry.affected_element
                == inject_fault_log_entry_as_dict["affected_element"]
            )
            assert (
                inject_fault_log_entry.value_before
                == inject_fault_log_entry_as_dict["value_before"]
            )
            assert (
                inject_fault_log_entry.value_after
                == inject_fault_log_entry_as_dict["value_after"]
            )

            assert inject_fault_log_entry.to_dict() == {
                "id": str(inject_fault_log_entry.id),
                # pylint: disable=no-member
                "created_at": inject_fault_log_entry.created_at.isoformat(),
                "updated_at": inject_fault_log_entry.updated_at.isoformat(),
                "timestamp": inject_fault_log_entry_as_dict["timestamp"].isoformat(),
                "tick": inject_fault_log_entry_as_dict["tick"],
                "message": inject_fault_log_entry_as_dict["message"],
                "run_id": str(inject_fault_log_entry_as_dict["run_id"]),
                "train_speed_fault_configuration": str(
                    inject_fault_log_entry_as_dict["train_speed_fault_configuration"]
                ),
                "platform_blocked_fault_configuration": str(
                    inject_fault_log_entry_as_dict[
                        "platform_blocked_fault_configuration"
                    ]
                ),
                "train_cancelled_fault_configuration": str(
                    inject_fault_log_entry_as_dict[
                        "train_cancelled_fault_configuration"
                    ]
                ),
                "affected_element": inject_fault_log_entry_as_dict["affected_element"],
                "value_before": inject_fault_log_entry_as_dict["value_before"],
                "value_after": inject_fault_log_entry_as_dict["value_after"],
            }

        def test_deserialization(self, inject_fault_log_entry_as_dict_serialized):
            """Test that Inject Fault Log Entry can be deserialized."""
            inject_fault_log_entry = InjectFaultLogEntry.Schema().load(
                inject_fault_log_entry_as_dict_serialized
            )
            assert isinstance(inject_fault_log_entry, InjectFaultLogEntry)
            assert isinstance(inject_fault_log_entry.id, UUID)
            assert isinstance(inject_fault_log_entry.timestamp, datetime)
            assert isinstance(inject_fault_log_entry.tick, int)
            assert isinstance(inject_fault_log_entry.message, str)
            assert isinstance(inject_fault_log_entry.run_id, Run)
            assert isinstance(
                inject_fault_log_entry.train_speed_fault_configuration,
                TrainSpeedFaultConfiguration,
            )
            assert isinstance(
                inject_fault_log_entry.platform_blocked_fault_configuration,
                PlatformBlockedFaultConfiguration,
            )
            assert isinstance(
                inject_fault_log_entry.train_cancelled_fault_configuration,
                TrainCancelledFaultConfiguration,
            )
            assert isinstance(inject_fault_log_entry.affected_element, str)
            assert isinstance(inject_fault_log_entry.value_before, str)
            assert isinstance(inject_fault_log_entry.value_after, str)

            assert (
                inject_fault_log_entry.timestamp.isoformat()
                == inject_fault_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                inject_fault_log_entry.tick
                == inject_fault_log_entry_as_dict_serialized["tick"]
            )
            assert (
                inject_fault_log_entry.message
                == inject_fault_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(inject_fault_log_entry.run_id)
                == inject_fault_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                str(inject_fault_log_entry.train_speed_fault_configuration)
                == inject_fault_log_entry_as_dict_serialized[
                    "train_speed_fault_configuration"
                ]
            )
            assert (
                str(inject_fault_log_entry.platform_blocked_fault_configuration)
                == inject_fault_log_entry_as_dict_serialized[
                    "platform_blocked_fault_configuration"
                ]
            )
            assert (
                str(inject_fault_log_entry.train_cancelled_fault_configuration)
                == inject_fault_log_entry_as_dict_serialized[
                    "train_cancelled_fault_configuration"
                ]
            )
            assert (
                inject_fault_log_entry.affected_element
                == inject_fault_log_entry_as_dict_serialized["affected_element"]
            )
            assert (
                inject_fault_log_entry.value_before
                == inject_fault_log_entry_as_dict_serialized["value_before"]
            )
            assert (
                inject_fault_log_entry.value_after
                == inject_fault_log_entry_as_dict_serialized["value_after"]
            )

        def test_deserialization_empty_fails(
            self, empty_inject_fault_log_entry_as_dict
        ):
            """Test that Inject Fault Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                InjectFaultLogEntry.Schema().load(empty_inject_fault_log_entry_as_dict)

    class TestResolveFaultLogEntry:
        """Tests for ResolveFaultLogEntry."""

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def resolve_fault_log_entry_as_dict(
            self,
            timestamp,
            tick,
            message,
            run,
            train_speed_fault_configuration,
            platform_blocked_fault_configuration,
            train_cancelled_fault_configuration,
        ):
            """ResolveFaultLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_speed_fault_configuration": train_speed_fault_configuration.id,
                "platform_blocked_fault_configuration": platform_blocked_fault_configuration.id,
                "train_cancelled_fault_configuration": train_cancelled_fault_configuration.id,
            }

        @pytest.fixture
        # pylint: disable=too-many-arguments
        def resolve_fault_log_entry_as_dict_serialized(
            self,
            timestamp,
            tick,
            message,
            run,
            train_speed_fault_configuration,
            platform_blocked_fault_configuration,
            train_cancelled_fault_configuration,
        ):
            """ResolveFaultLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_speed_fault_configuration": str(
                    train_speed_fault_configuration.id
                ),
                "platform_blocked_fault_configuration": str(
                    platform_blocked_fault_configuration.id
                ),
                "train_cancelled_fault_configuration": str(
                    train_cancelled_fault_configuration.id
                ),
            }

        @pytest.fixture
        def empty_resolve_fault_log_entry_as_dict(self):
            """ResolveFaultLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, resolve_fault_log_entry_as_dict):
            """Test that Remove Fault Log Entry can be created."""
            resolve_fault_log_entry = ResolveFaultLogEntry.create(
                **resolve_fault_log_entry_as_dict
            )
            assert (
                ResolveFaultLogEntry.select()
                .where(ResolveFaultLogEntry.id == resolve_fault_log_entry.id)
                .first()
                == resolve_fault_log_entry
            )

        def test_create_empty_fails(self, empty_resolve_fault_log_entry_as_dict):
            """Test that Remove Fault Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                ResolveFaultLogEntry.create(**empty_resolve_fault_log_entry_as_dict)

        def test_serialization(self, resolve_fault_log_entry_as_dict):
            """Test that Remove Fault Log Entry can be serialized."""
            resolve_fault_log_entry = ResolveFaultLogEntry.create(
                **resolve_fault_log_entry_as_dict
            )
            assert (
                resolve_fault_log_entry.timestamp
                == resolve_fault_log_entry_as_dict["timestamp"]
            )
            assert (
                resolve_fault_log_entry.tick == resolve_fault_log_entry_as_dict["tick"]
            )
            assert (
                resolve_fault_log_entry.message
                == resolve_fault_log_entry_as_dict["message"]
            )
            assert (
                resolve_fault_log_entry.run_id.id
                == resolve_fault_log_entry_as_dict["run_id"]
            )
            assert (
                resolve_fault_log_entry.train_speed_fault_configuration.id
                == resolve_fault_log_entry_as_dict["train_speed_fault_configuration"]
            )
            assert (
                resolve_fault_log_entry.platform_blocked_fault_configuration.id
                == resolve_fault_log_entry_as_dict[
                    "platform_blocked_fault_configuration"
                ]
            )
            assert (
                resolve_fault_log_entry.train_cancelled_fault_configuration.id
                == resolve_fault_log_entry_as_dict[
                    "train_cancelled_fault_configuration"
                ]
            )

            assert resolve_fault_log_entry.to_dict() == {
                "id": str(resolve_fault_log_entry.id),
                # pylint: disable=no-member
                "created_at": resolve_fault_log_entry.created_at.isoformat(),
                "updated_at": resolve_fault_log_entry.updated_at.isoformat(),
                "timestamp": resolve_fault_log_entry_as_dict["timestamp"].isoformat(),
                "tick": resolve_fault_log_entry_as_dict["tick"],
                "message": resolve_fault_log_entry_as_dict["message"],
                "run_id": str(resolve_fault_log_entry_as_dict["run_id"]),
                "train_speed_fault_configuration": str(
                    resolve_fault_log_entry_as_dict["train_speed_fault_configuration"]
                ),
                "platform_blocked_fault_configuration": str(
                    resolve_fault_log_entry_as_dict[
                        "platform_blocked_fault_configuration"
                    ]
                ),
                "train_cancelled_fault_configuration": str(
                    resolve_fault_log_entry_as_dict[
                        "train_cancelled_fault_configuration"
                    ]
                ),
            }

        def test_deserialization(self, resolve_fault_log_entry_as_dict_serialized):
            """Test that Remove Fault Log Entry can be deserialized."""
            resolve_fault_log_entry = ResolveFaultLogEntry.Schema().load(
                resolve_fault_log_entry_as_dict_serialized
            )
            assert isinstance(resolve_fault_log_entry, ResolveFaultLogEntry)
            assert isinstance(resolve_fault_log_entry.id, UUID)
            assert isinstance(resolve_fault_log_entry.timestamp, datetime)
            assert isinstance(resolve_fault_log_entry.tick, int)
            assert isinstance(resolve_fault_log_entry.message, str)
            assert isinstance(resolve_fault_log_entry.run_id, Run)
            assert isinstance(
                resolve_fault_log_entry.train_speed_fault_configuration,
                TrainSpeedFaultConfiguration,
            )
            assert isinstance(
                resolve_fault_log_entry.platform_blocked_fault_configuration,
                PlatformBlockedFaultConfiguration,
            )
            assert isinstance(
                resolve_fault_log_entry.train_cancelled_fault_configuration,
                TrainCancelledFaultConfiguration,
            )
            assert (
                resolve_fault_log_entry.timestamp.isoformat()
                == resolve_fault_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                resolve_fault_log_entry.tick
                == resolve_fault_log_entry_as_dict_serialized["tick"]
            )
            assert (
                resolve_fault_log_entry.message
                == resolve_fault_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(resolve_fault_log_entry.run_id)
                == resolve_fault_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                str(resolve_fault_log_entry.train_speed_fault_configuration)
                == resolve_fault_log_entry_as_dict_serialized[
                    "train_speed_fault_configuration"
                ]
            )
            assert (
                str(resolve_fault_log_entry.platform_blocked_fault_configuration)
                == resolve_fault_log_entry_as_dict_serialized[
                    "platform_blocked_fault_configuration"
                ]
            )
            assert (
                str(resolve_fault_log_entry.train_cancelled_fault_configuration)
                == resolve_fault_log_entry_as_dict_serialized[
                    "train_cancelled_fault_configuration"
                ]
            )

        def test_deserialization_empty_fails(
            self, empty_resolve_fault_log_entry_as_dict
        ):
            """Test that Remove Fault Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                ResolveFaultLogEntry.Schema().load(
                    empty_resolve_fault_log_entry_as_dict
                )
