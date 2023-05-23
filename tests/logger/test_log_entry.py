# pylint: disable=too-many-lines
from datetime import datetime
from uuid import UUID

import pytest
from marshmallow import ValidationError
from peewee import IntegrityError

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
from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    InjectFaultLogEntry,
    LogEntry,
    RemoveFahrstrasseLogEntry,
    ResolveFaultLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainEnterBlockSectionLogEntry,
    TrainLeaveBlockSectionLogEntry,
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

    class TestTrainSpawnLogEntry:
        """Tests for TrainSpawnLogEntry."""

        @pytest.fixture
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

    class TestTrainRemoveLogEntry:
        """Tests for TrainRemoveLogEntry."""

        @pytest.fixture
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

    class TestTrainArrivalLogEntry:
        """Tests for TrainArrivalLogEntry."""

        @pytest.fixture
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

    class TestTrainDepartureLogEntry:
        """Tests for the Train Departure Log Entry."""

        @pytest.fixture
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

    class TestCreateFahrstrasseLogEntry:
        """Tests for CreateFahrstrasseLogEntry."""

        @pytest.fixture
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

    class TestRemoveFahrstrasseLogEntry:
        """Tests for RemoveFahrstrasseLogEntry."""

        @pytest.fixture
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

    class TestSignalLogEntry:
        """Tests for SignalLogEntry."""

        @pytest.fixture
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

    class TestTrainEnterBlockSectionLogEntry:
        """Tests for TrainEnterBlockSectionLogEntry."""

        @pytest.fixture
        def train_enter_block_section_log_entry_as_dict(
            self,
            timestamp,
            tick,
            message,
            run,
            train_id,
            block_section_id,
            block_section_length,
        ):
            """TrainEnterBlockSectionLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
                "block_section_id": block_section_id,
                "block_section_length": block_section_length,
            }

        @pytest.fixture
        def train_enter_block_section_log_entry_as_dict_serialized(
            self,
            timestamp,
            tick,
            message,
            run,
            train_id,
            block_section_id,
            block_section_length,
        ):
            """TrainEnterBlockSectionLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_id": train_id,
                "block_section_id": block_section_id,
                "block_section_length": block_section_length,
            }

        @pytest.fixture
        def empty_train_enter_block_section_log_entry_as_dict(self):
            """TrainEnterBlockSectionLogEntry as dict with no fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, train_enter_block_section_log_entry_as_dict):
            """Test that TrainEnterBlockSectionLogEntry can be created."""
            train_enter_block_section_log_entry = TrainEnterBlockSectionLogEntry.create(
                **train_enter_block_section_log_entry_as_dict
            )
            assert (
                TrainEnterBlockSectionLogEntry.select()
                .where(
                    TrainEnterBlockSectionLogEntry.id
                    == train_enter_block_section_log_entry.id
                )
                .first()
                == train_enter_block_section_log_entry
            )

        def test_create_empty_fails(
            self, empty_train_enter_block_section_log_entry_as_dict
        ):
            """Tests that TrainEnterBlockSectionLogEntry cannot be created with no fields set."""
            with pytest.raises(IntegrityError):
                TrainEnterBlockSectionLogEntry.create(
                    **empty_train_enter_block_section_log_entry_as_dict
                )

    class TestTrainLeaveBlockSectionLogEntry:
        """Tests for TrainLeaveBlockSectionLogEntry."""

        @pytest.fixture
        def train_leave_block_section_log_entry_as_dict(
            self,
            timestamp,
            tick,
            message,
            run,
            train_id,
            block_section_id,
        ):
            """TrainLeaveBlockSectionLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "train_id": train_id,
                "block_section_id": block_section_id,
            }

        @pytest.fixture
        def train_leave_block_section_log_entry_as_dict_serialized(
            self,
            timestamp,
            tick,
            message,
            run,
            train_id,
            block_section_id,
        ):
            """TrainLeaveBlockSectionLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "train_id": train_id,
                "block_section_id": block_section_id,
            }

        @pytest.fixture
        def empty_train_leave_block_section_log_entry_as_dict(self):
            """TrainLeaveBlockSectionLogEntry as dict with all fields set."""
            return {}

        @recreate_db_setup
        def setup_method(self):
            pass

        def test_create(self, train_leave_block_section_log_entry_as_dict):
            """Test that TrainLeaveBlockSectionLogEntry can be created."""
            train_leave_block_section_log_entry = TrainLeaveBlockSectionLogEntry.create(
                **train_leave_block_section_log_entry_as_dict
            )
            assert (
                TrainLeaveBlockSectionLogEntry.select()
                .where(
                    TrainLeaveBlockSectionLogEntry.id
                    == train_leave_block_section_log_entry.id
                )
                .first()
                == train_leave_block_section_log_entry
            )

        def test_create_empty_fails(
            self, empty_train_leave_block_section_log_entry_as_dict
        ):
            """Test that TrainLeaveBlockSectionLogEntry cannot be created with empty dict."""
            with pytest.raises(IntegrityError):
                TrainLeaveBlockSectionLogEntry.create(
                    **empty_train_leave_block_section_log_entry_as_dict
                )

    class TestInjectFaultLogEntry:
        """Tests for InjectFaultLogEntry."""

        @pytest.fixture
        def inject_fault_log_entry_as_dict(
            self,
            timestamp,
            tick,
            message,
            run,
            platform_blocked_fault_configuration,
            track_blocked_fault_configuration,
            track_speed_limit_fault_configuration,
            schedule_blocked_fault_configuration,
            train_prio_fault_configuration,
            train_speed_fault_configuration,
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
                "platform_blocked_fault_configuration": platform_blocked_fault_configuration.id,
                "track_blocked_fault_configuration": track_blocked_fault_configuration.id,
                "track_speed_limit_fault_configuration": track_speed_limit_fault_configuration.id,
                "schedule_blocked_fault_configuration": schedule_blocked_fault_configuration.id,
                "train_prio_fault_configuration": train_prio_fault_configuration.id,
                "train_speed_fault_configuration": train_speed_fault_configuration.id,
                "affected_element": affected_element,
                "value_before": value_before,
                "value_after": value_after,
            }

        @pytest.fixture
        def inject_fault_log_entry_as_dict_serialized(
            self,
            timestamp,
            tick,
            message,
            run,
            platform_blocked_fault_configuration,
            track_blocked_fault_configuration,
            track_speed_limit_fault_configuration,
            schedule_blocked_fault_configuration,
            train_prio_fault_configuration,
            train_speed_fault_configuration,
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
                "platform_blocked_fault_configuration": str(
                    platform_blocked_fault_configuration.id
                ),
                "track_blocked_fault_configuration": str(
                    track_blocked_fault_configuration.id
                ),
                "track_speed_limit_fault_configuration": str(
                    track_speed_limit_fault_configuration.id
                ),
                "schedule_blocked_fault_configuration": str(
                    schedule_blocked_fault_configuration.id
                ),
                "train_prio_fault_configuration": str(
                    train_prio_fault_configuration.id
                ),
                "train_speed_fault_configuration": str(
                    train_speed_fault_configuration.id
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

    class TestResolveFaultLogEntry:
        """Tests for ResolveFaultLogEntry."""

        @pytest.fixture
        def resolve_fault_log_entry_as_dict(
            self,
            timestamp,
            tick,
            message,
            run,
            platform_blocked_fault_configuration,
            track_blocked_fault_configuration,
            track_speed_limit_fault_configuration,
            schedule_blocked_fault_configuration,
            train_prio_fault_configuration,
            train_speed_fault_configuration,
        ):
            """ResolveFaultLogEntry as dict with all fields set."""
            return {
                "timestamp": timestamp,
                "tick": tick,
                "message": message,
                "run_id": run.id,
                "platform_blocked_fault_configuration": platform_blocked_fault_configuration.id,
                "track_blocked_fault_configuration": track_blocked_fault_configuration.id,
                "track_speed_limit_fault_configuration": track_speed_limit_fault_configuration.id,
                "schedule_blocked_fault_configuration": schedule_blocked_fault_configuration.id,
                "train_prio_fault_configuration": train_prio_fault_configuration.id,
                "train_speed_fault_configuration": train_speed_fault_configuration.id,
            }

        @pytest.fixture
        def resolve_fault_log_entry_as_dict_serialized(
            self,
            timestamp,
            tick,
            message,
            run,
            platform_blocked_fault_configuration,
            track_blocked_fault_configuration,
            track_speed_limit_fault_configuration,
            schedule_blocked_fault_configuration,
            train_prio_fault_configuration,
            train_speed_fault_configuration,
        ):
            """ResolveFaultLogEntry as serialized dict with all fields set."""
            return {
                "timestamp": timestamp.isoformat(),
                "tick": tick,
                "message": message,
                "run_id": str(run.id),
                "platform_blocked_fault_configuration": str(
                    platform_blocked_fault_configuration.id
                ),
                "track_blocked_fault_configuration": str(
                    track_blocked_fault_configuration.id
                ),
                "track_speed_limit_fault_configuration": str(
                    track_speed_limit_fault_configuration.id
                ),
                "schedule_blocked_fault_configuration": str(
                    schedule_blocked_fault_configuration.id
                ),
                "train_prio_fault_configuration": str(
                    train_prio_fault_configuration.id
                ),
                "train_speed_fault_configuration": str(
                    train_speed_fault_configuration.id
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
