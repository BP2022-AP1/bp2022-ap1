from datetime import datetime
from uuid import UUID

import pytest
from marshmallow import ValidationError
from peewee import IntegrityError

from src.implementor.models import Run
from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    InjectFaultLogEntry,
    LogEntry,
    RemoveFahrstrasseLogEntry,
    RemoveFaultLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)
from tests.decorators import recreate_db_setup


class TestLogEntry:
    """Class for testing all LogEntry classes."""
    @pytest.fixture
    def timestamp(self):
        return datetime.strptime("2023-04-11-10-00-00", "%Y-%m-%d-%H-%M-%S")

    @pytest.fixture
    def message(self):
        return "Test Log Done"

    @pytest.fixture
    def run_as_dict(self):
        return {}

    @pytest.fixture
    def run(self, run_as_dict):
        return Run.create(**run_as_dict)

    @pytest.fixture
    def train_id(self):
        return 123

    @pytest.fixture
    def station_id(self):
        return 456

    @pytest.fixture
    def fahrstrasse(self):
        return "Test Fahrstrasse"

    @pytest.fixture
    def signal_id(self):
        return "Test Signal"

    @pytest.fixture
    def state_before(self):
        return 0

    @pytest.fixture
    def state_after(self):
        return 1

    @pytest.fixture
    def injection_id(self):
        return 123

    @pytest.fixture
    def fault_type(self):
        return 3

    @pytest.fixture
    def injection_position(self):
        return "Test Position"

    @pytest.fixture
    def duration(self):
        return 10

    class TestLogEntry:
        """Test LogEntry."""

        @pytest.fixture
        def log_entry_as_dict(self, timestamp, message, run):
            """LogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
            }

        @pytest.fixture
        def log_entry_as_dict_serialized(self, timestamp, message, run):
            """LogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
            assert log_entry.message == log_entry_as_dict["message"]
            assert log_entry.run_id.id == log_entry_as_dict["run_id"]

            assert log_entry.to_dict() == {
                "id": str(log_entry.id),
                "timestamp": log_entry_as_dict["timestamp"].isoformat(),
                "message": log_entry_as_dict["message"],
                "run_id": str(log_entry_as_dict["run_id"]),
            }

        def test_deserialization(self, log_entry_as_dict_serialized):
            """Test that Log Entry can be deserialized."""
            log_entry = LogEntry.Schema().load(log_entry_as_dict_serialized)
            assert isinstance(log_entry, LogEntry)
            assert isinstance(log_entry.id, UUID)
            assert isinstance(log_entry.timestamp, datetime)
            assert isinstance(log_entry.message, str)
            assert isinstance(log_entry.run_id, Run)
            assert (
                log_entry.timestamp.isoformat()
                == log_entry_as_dict_serialized["timestamp"]
            )
            assert log_entry.message == log_entry_as_dict_serialized["message"]
            assert str(log_entry.run_id) == log_entry_as_dict_serialized["run_id"]

        def test_deserialization_empty_fails(self, empty_log_entry_as_dict):
            """Test that Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                LogEntry.Schema().load(empty_log_entry_as_dict)

    class TestTrainSpawnLogEntry:
        """Tests for TrainSpawnLogEntry."""
        @pytest.fixture
        def train_spawn_log_entry_as_dict(self, timestamp, message, run, train_id):
            """TrainSpawnLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
            }

        @pytest.fixture
        def train_spawn_log_entry_as_dict_serialized(
            self, timestamp, message, run, train_id
        ):
            """TrainSpawnLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
                "timestamp": train_spawn_log_entry_as_dict["timestamp"].isoformat(),
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
            assert isinstance(train_spawn_log_entry.message, str)
            assert isinstance(train_spawn_log_entry.run_id, Run)
            assert isinstance(train_spawn_log_entry.train_id, int)
            assert (
                train_spawn_log_entry.timestamp.isoformat()
                == train_spawn_log_entry_as_dict_serialized["timestamp"]
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
        def train_remove_log_entry_as_dict(self, timestamp, message, run, train_id):
            """TrainRemoveLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
            }

        @pytest.fixture
        def train_remove_log_entry_as_dict_serialized(
            self, timestamp, message, run, train_id
        ):
            """TrainRemoveLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
                "timestamp": train_remove_log_entry_as_dict["timestamp"].isoformat(),
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
            assert isinstance(train_remove_log_entry.message, str)
            assert isinstance(train_remove_log_entry.run_id, Run)
            assert isinstance(train_remove_log_entry.train_id, int)
            assert (
                train_remove_log_entry.timestamp.isoformat()
                == train_remove_log_entry_as_dict_serialized["timestamp"]
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
        def train_arrival_log_entry_as_dict(
            self, timestamp, message, run, train_id, station_id
        ):
            """TrainArrivalLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
                "station_id": station_id,
            }

        @pytest.fixture
        def train_arrival_log_entry_as_dict_serialized(
            self, timestamp, message, run, train_id, station_id
        ):
            """TrainArrivalLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
                "timestamp": train_arrival_log_entry_as_dict["timestamp"].isoformat(),
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
            assert isinstance(train_arrival_log_entry.message, str)
            assert isinstance(train_arrival_log_entry.run_id, Run)
            assert isinstance(train_arrival_log_entry.train_id, int)
            assert isinstance(train_arrival_log_entry.station_id, int)
            assert (
                train_arrival_log_entry.timestamp.isoformat()
                == train_arrival_log_entry_as_dict_serialized["timestamp"]
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
        def train_departure_log_entry_as_dict(
            self, timestamp, message, run, train_id, station_id
        ):
            """TrainDepartureLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
                "station_id": station_id,
            }

        @pytest.fixture
        def train_departure_log_entry_as_dict_serialized(
            self, timestamp, message, run, train_id, station_id
        ):
            """TrainDepartureLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
                "timestamp": train_departure_log_entry_as_dict["timestamp"].isoformat(),
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
            assert isinstance(train_departure_log_entry.message, str)
            assert isinstance(train_departure_log_entry.run_id, Run)
            assert isinstance(train_departure_log_entry.train_id, int)
            assert isinstance(train_departure_log_entry.station_id, int)
            assert (
                train_departure_log_entry.timestamp.isoformat()
                == train_departure_log_entry_as_dict_serialized["timestamp"]
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
        def create_fahrstrasse_log_entry_as_dict(
            self, timestamp, message, run, fahrstrasse
        ):
            """CreateFahrstrasseLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "fahrstrasse": fahrstrasse,
            }

        @pytest.fixture
        def create_fahrstrasse_log_entry_as_dict_serialized(
            self, timestamp, message, run, fahrstrasse
        ):
            """CreateFahrstrasseLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
                "timestamp": create_fahrstrasse_log_entry_as_dict[
                    "timestamp"
                ].isoformat(),
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
            assert isinstance(create_fahrstrasse_log_entry.message, str)
            assert isinstance(create_fahrstrasse_log_entry.run_id, Run)
            assert isinstance(create_fahrstrasse_log_entry.fahrstrasse, str)
            assert (
                create_fahrstrasse_log_entry.timestamp.isoformat()
                == create_fahrstrasse_log_entry_as_dict_serialized["timestamp"]
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
        def remove_fahrstrasse_log_entry_as_dict(
            self, timestamp, message, run, fahrstrasse
        ):
            """RemoveFahrstrasseLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "fahrstrasse": fahrstrasse,
            }

        @pytest.fixture
        def remove_fahrstrasse_log_entry_as_dict_serialized(
            self, timestamp, message, run, fahrstrasse
        ):
            """RemoveFahrstrasseLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
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
                "timestamp": remove_fahrstrasse_log_entry_as_dict[
                    "timestamp"
                ].isoformat(),
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
            assert isinstance(remove_fahrstrasse_log_entry.message, str)
            assert isinstance(remove_fahrstrasse_log_entry.run_id, Run)
            assert isinstance(remove_fahrstrasse_log_entry.fahrstrasse, str)
            assert (
                remove_fahrstrasse_log_entry.timestamp.isoformat()
                == remove_fahrstrasse_log_entry_as_dict_serialized["timestamp"]
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
        def set_signal_log_entry_as_dict(
            self, timestamp, message, run, signal_id, state_before, state_after
        ):
            """SetSignalLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "signal_id": signal_id,
                "state_before": state_before,
                "state_after": state_after,
            }

        @pytest.fixture
        def set_signal_log_entry_as_dict_serialized(
            self, timestamp, message, run, signal_id, state_before, state_after
        ):
            """SetSignalLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "message": message,
                "run_id": str(run.id),
                "signal_id": signal_id,
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
                "timestamp": set_signal_log_entry_as_dict["timestamp"].isoformat(),
                "message": set_signal_log_entry_as_dict["message"],
                "run_id": str(set_signal_log_entry_as_dict["run_id"]),
                "signal_id": set_signal_log_entry_as_dict["signal_id"],
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
            assert isinstance(set_signal_log_entry.message, str)
            assert isinstance(set_signal_log_entry.run_id, Run)
            assert isinstance(set_signal_log_entry.signal_id, str)
            assert isinstance(set_signal_log_entry.state_before, int)
            assert isinstance(set_signal_log_entry.state_after, int)
            assert (
                set_signal_log_entry.timestamp.isoformat()
                == set_signal_log_entry_as_dict_serialized["timestamp"]
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
                set_signal_log_entry.signal_id
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
        def inject_fault_log_entry_as_dict(
            self,
            timestamp,
            message,
            run,
            injection_id,
            fault_type,
            injection_position,
            duration,
        ):
            """InjectFaultLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "injection_id": injection_id,
                "fault_type": fault_type,
                "injection_position": injection_position,
                "duration": duration,
            }

        @pytest.fixture
        def inject_fault_log_entry_as_dict_serialized(
            self,
            timestamp,
            message,
            run,
            injection_id,
            fault_type,
            injection_position,
            duration,
        ):
            """InjectFaultLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "message": message,
                "run_id": str(run.id),
                "injection_id": injection_id,
                "fault_type": fault_type,
                "injection_position": injection_position,
                "duration": duration,
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
            assert (
                inject_fault_log_entry.message
                == inject_fault_log_entry_as_dict["message"]
            )
            assert (
                inject_fault_log_entry.run_id.id
                == inject_fault_log_entry_as_dict["run_id"]
            )
            assert (
                inject_fault_log_entry.injection_id
                == inject_fault_log_entry_as_dict["injection_id"]
            )
            assert (
                inject_fault_log_entry.fault_type
                == inject_fault_log_entry_as_dict["fault_type"]
            )
            assert (
                inject_fault_log_entry.injection_position
                == inject_fault_log_entry_as_dict["injection_position"]
            )
            assert (
                inject_fault_log_entry.duration
                == inject_fault_log_entry_as_dict["duration"]
            )

            assert inject_fault_log_entry.to_dict() == {
                "id": str(inject_fault_log_entry.id),
                "timestamp": inject_fault_log_entry.timestamp.isoformat(),
                "message": inject_fault_log_entry.message,
                "run_id": str(inject_fault_log_entry.run_id),
                "injection_id": inject_fault_log_entry.injection_id,
                "fault_type": inject_fault_log_entry.fault_type,
                "injection_position": inject_fault_log_entry.injection_position,
                "duration": inject_fault_log_entry.duration,
            }

        def test_deserialization(self, inject_fault_log_entry_as_dict_serialized):
            """Test that Inject Fault Log Entry can be deserialized."""
            inject_fault_log_entry = InjectFaultLogEntry.Schema().load(
                inject_fault_log_entry_as_dict_serialized
            )
            assert isinstance(inject_fault_log_entry, InjectFaultLogEntry)
            assert isinstance(inject_fault_log_entry.id, UUID)
            assert isinstance(inject_fault_log_entry.timestamp, datetime)
            assert isinstance(inject_fault_log_entry.message, str)
            assert isinstance(inject_fault_log_entry.run_id, Run)
            assert isinstance(inject_fault_log_entry.injection_id, int)
            assert isinstance(inject_fault_log_entry.fault_type, int)
            assert isinstance(inject_fault_log_entry.injection_position, str)
            assert isinstance(inject_fault_log_entry.duration, int)
            assert (
                inject_fault_log_entry.timestamp.isoformat()
                == inject_fault_log_entry_as_dict_serialized["timestamp"]
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
                inject_fault_log_entry.injection_id
                == inject_fault_log_entry_as_dict_serialized["injection_id"]
            )
            assert (
                inject_fault_log_entry.fault_type
                == inject_fault_log_entry_as_dict_serialized["fault_type"]
            )
            assert (
                inject_fault_log_entry.injection_position
                == inject_fault_log_entry_as_dict_serialized["injection_position"]
            )
            assert (
                inject_fault_log_entry.duration
                == inject_fault_log_entry_as_dict_serialized["duration"]
            )

        def test_deserialization_empty_fails(
            self, empty_inject_fault_log_entry_as_dict
        ):
            """Test that Inject Fault Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                InjectFaultLogEntry.Schema().load(empty_inject_fault_log_entry_as_dict)

    class TestRemoveFaultLogEntry:
        """Tests for RemoveFaultLogEntry."""
        @pytest.fixture
        def remove_fault_log_entry_as_dict(self, timestamp, message, run, injection_id):
            """RemoveFaultLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "message": message,
                "run_id": run.id,
                "injection_id": injection_id,
            }

        @pytest.fixture
        def remove_fault_log_entry_as_dict_serialized(
            self, timestamp, message, run, injection_id
        ):
            """RemoveFaultLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "message": message,
                "run_id": str(run.id),
                "injection_id": injection_id,
            }

        @pytest.fixture
        def empty_remove_fault_log_entry_as_dict(self):
            """RemoveFaultLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, remove_fault_log_entry_as_dict):
            """Test that Remove Fault Log Entry can be created."""
            remove_fault_log_entry = RemoveFaultLogEntry.create(
                **remove_fault_log_entry_as_dict
            )
            assert (
                RemoveFaultLogEntry.select()
                .where(RemoveFaultLogEntry.id == remove_fault_log_entry.id)
                .first()
                == remove_fault_log_entry
            )

        def test_create_empty_fails(self, empty_remove_fault_log_entry_as_dict):
            """Test that Remove Fault Log Entry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                RemoveFaultLogEntry.create(**empty_remove_fault_log_entry_as_dict)

        def test_serialization(self, remove_fault_log_entry_as_dict):
            """Test that Remove Fault Log Entry can be serialized."""
            remove_fault_log_entry = RemoveFaultLogEntry.create(
                **remove_fault_log_entry_as_dict
            )
            assert (
                remove_fault_log_entry.timestamp
                == remove_fault_log_entry_as_dict["timestamp"]
            )
            assert (
                remove_fault_log_entry.message
                == remove_fault_log_entry_as_dict["message"]
            )
            assert (
                remove_fault_log_entry.run_id.id
                == remove_fault_log_entry_as_dict["run_id"]
            )
            assert (
                remove_fault_log_entry.injection_id
                == remove_fault_log_entry_as_dict["injection_id"]
            )

            assert remove_fault_log_entry.to_dict() == {
                "id": str(remove_fault_log_entry.id),
                "timestamp": remove_fault_log_entry.timestamp.isoformat(),
                "message": remove_fault_log_entry.message,
                "run_id": str(remove_fault_log_entry.run_id.id),
                "injection_id": remove_fault_log_entry.injection_id,
            }

        def test_deserialization(self, remove_fault_log_entry_as_dict_serialized):
            """Test that Remove Fault Log Entry can be deserialized."""
            remove_fault_log_entry = RemoveFaultLogEntry.Schema().load(
                remove_fault_log_entry_as_dict_serialized
            )
            assert isinstance(remove_fault_log_entry, RemoveFaultLogEntry)
            assert isinstance(remove_fault_log_entry.id, UUID)
            assert isinstance(remove_fault_log_entry.timestamp, datetime)
            assert isinstance(remove_fault_log_entry.message, str)
            assert isinstance(remove_fault_log_entry.run_id, Run)
            assert isinstance(remove_fault_log_entry.injection_id, int)
            assert (
                remove_fault_log_entry.timestamp.isoformat()
                == remove_fault_log_entry_as_dict_serialized["timestamp"]
            )
            assert (
                remove_fault_log_entry.message
                == remove_fault_log_entry_as_dict_serialized["message"]
            )
            assert (
                str(remove_fault_log_entry.run_id)
                == remove_fault_log_entry_as_dict_serialized["run_id"]
            )
            assert (
                remove_fault_log_entry.injection_id
                == remove_fault_log_entry_as_dict_serialized["injection_id"]
            )

        def test_deserialization_empty_fails(
            self, empty_remove_fault_log_entry_as_dict
        ):
            """Test that Remove Fault Log Entry cannot be deserialized with no fields set."""
            with pytest.raises(ValidationError):
                RemoveFaultLogEntry.Schema().load(empty_remove_fault_log_entry_as_dict)
