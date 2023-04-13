from datetime import datetime

from freezegun import freeze_time

from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    InjectFaultLogEntry,
    RemoveFahrstrasseLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)
from src.logger.logger import Logger
from tests.decorators import recreate_db_setup


class TestLogger:
    """Class for testing logger functions."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @freeze_time()
    def test_spawn_train(self, run, tick, train_id):
        logger = Logger(run_id=run.id)
        logger.spawn_train(tick=tick, train_id=train_id)
        log_entry = (
            TrainSpawnLogEntry.select()
            .where(TrainSpawnLogEntry.train_id == train_id)
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Train with ID {train_id} spawned"
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id

    @freeze_time()
    def test_remove_train(self, run, tick, train_id):
        logger = Logger(run_id=run.id)
        logger.remove_train(tick=tick, train_id=train_id)
        log_entry = (
            TrainRemoveLogEntry.select()
            .where(TrainRemoveLogEntry.train_id == train_id)
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Train with ID {train_id} removed"
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id

    @freeze_time()
    def test_arrival_train(self, run, tick, train_id, station_id):
        logger = Logger(run_id=run.id)
        logger.arrival_train(tick=tick, train_id=train_id, station_id=station_id)
        log_entry = (
            TrainArrivalLogEntry.select()
            .where(
                TrainArrivalLogEntry.tick == tick
                and TrainArrivalLogEntry.train_id == train_id
                and TrainArrivalLogEntry.station_id == station_id
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train with ID {train_id} arrived at station with ID {station_id}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
        assert log_entry.station_id == station_id

    @freeze_time()
    def test_departure_train(self, run, tick, train_id, station_id):
        logger = Logger(run_id=run.id)
        logger.departure_train(tick=tick, train_id=train_id, station_id=station_id)
        log_entry = (
            TrainDepartureLogEntry.select()
            .where(
                TrainRemoveLogEntry.tick == tick
                and TrainDepartureLogEntry.train_id == train_id
                and TrainDepartureLogEntry.station_id == station_id
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train with ID {train_id} departed from station with ID {station_id}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
        assert log_entry.station_id == station_id

    @freeze_time()
    def test_create_fahrstrasse(self, run, tick, fahrstrasse):
        logger = Logger(run_id=run.id)
        logger.create_fahrstrasse(tick=tick, fahrstrasse=fahrstrasse)
        log_entry = (
            CreateFahrstrasseLogEntry.select()
            .where(
                CreateFahrstrasseLogEntry.tick == tick
                and CreateFahrstrasseLogEntry.fahrstrasse == fahrstrasse
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Fahrstrasse {fahrstrasse} created"
        assert log_entry.run_id.id == run.id
        assert log_entry.fahrstrasse == fahrstrasse

    @freeze_time()
    def test_remove_fahrstrasse(self, run, tick, fahrstrasse):
        logger = Logger(run_id=run.id)
        logger.remove_fahrstrasse(tick=tick, fahrstrasse=fahrstrasse)
        log_entry = (
            RemoveFahrstrasseLogEntry.select()
            .where(
                RemoveFahrstrasseLogEntry.tick == tick
                and RemoveFahrstrasseLogEntry.fahrstrasse == fahrstrasse
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Fahrstrasse {fahrstrasse} removed"
        assert log_entry.run_id.id == run.id
        assert log_entry.fahrstrasse == fahrstrasse

    @freeze_time()
    def test_set_signal(self, run, tick, signal_id, state_before, state_after):
        logger = Logger(run_id=run.id)
        logger.set_signal(
            tick=tick,
            signal_id=signal_id,
            state_before=state_before,
            state_after=state_after,
        )
        log_entry = (
            SetSignalLogEntry.select()
            .where(
                SetSignalLogEntry.tick == tick
                and SetSignalLogEntry.signal_id == signal_id
                and SetSignalLogEntry.state_before == state_before
                and SetSignalLogEntry.state_after == state_after
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Signal with ID {signal_id} changed from {state_before} to {state_after}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.signal_id == signal_id
        assert log_entry.state_before == state_before
        assert log_entry.state_after == state_after

    @freeze_time()
    def test_inject_platform_blocked_fault(
        self,
        run,
        tick,
        platform_blocked_fault_configuration,
        affected_element,
    ):
        logger = Logger(run_id=run.id)
        logger.inject_platform_blocked_fault(
            tick=tick,
            platform_blocked_fault_configuration=platform_blocked_fault_configuration,
            affected_element=affected_element,
        )
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                InjectFaultLogEntry.tick == tick
                and InjectFaultLogEntry.platform_blocked_fault_configuration
                == platform_blocked_fault_configuration
                and InjectFaultLogEntry.affected_element == affected_element
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Platform blocked fault with configuration {platform_blocked_fault_configuration} "
            f"on element {affected_element}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.platform_blocked_fault_configuration
            == platform_blocked_fault_configuration
        )
        assert log_entry.affected_element == affected_element

        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_track_blocked_fault(
        self,
        run,
        tick,
        track_blocked_fault_configuration,
        affected_element,
    ):
        logger = Logger(run_id=run.id)
        logger.inject_track_blocked_fault(
            tick=tick,
            track_blocked_fault_configuration=track_blocked_fault_configuration,
            affected_element=affected_element,
        )
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                InjectFaultLogEntry.tick == tick
                and InjectFaultLogEntry.track_blocked_fault_configuration
                == track_blocked_fault_configuration
                and InjectFaultLogEntry.affected_element == affected_element
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Track blocked fault with configuration {track_blocked_fault_configuration} "
            f"on element {affected_element}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.track_blocked_fault_configuration
            == track_blocked_fault_configuration
        )
        assert log_entry.affected_element == affected_element

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_track_speed_limit_fault(
        self,
        run,
        tick,
        track_speed_limit_fault_configuration,
        affected_element,
        value_before,
        value_after,
    ):
        logger = Logger(run_id=run.id)
        logger.inject_track_speed_limit_fault(
            tick=tick,
            track_speed_limit_fault_configuration=track_speed_limit_fault_configuration,
            affected_element=affected_element,
            value_before=value_before,
            value_after=value_after,
        )
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                InjectFaultLogEntry.tick == tick
                and InjectFaultLogEntry.track_speed_limit_fault_configuration
                == track_speed_limit_fault_configuration
                and InjectFaultLogEntry.affected_element == affected_element
                and InjectFaultLogEntry.value_before == value_before
                and InjectFaultLogEntry.value_after == value_after
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message == f"Track speed limit fault with configuration "
            f"{track_speed_limit_fault_configuration} on element {affected_element} changed "
            f"from {value_before} to {value_after}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.track_speed_limit_fault_configuration
            == track_speed_limit_fault_configuration
        )
        assert log_entry.affected_element == affected_element
        assert log_entry.value_before == value_before
        assert log_entry.value_after == value_after

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_schedule_blocked_fault(
        self,
        run,
        tick,
        schedule_blocked_fault_configuration,
        affected_element,
    ):
        logger = Logger(run_id=run.id)
        logger.inject_schedule_blocked_fault(
            tick=tick,
            schedule_blocked_fault_configuration=schedule_blocked_fault_configuration,
            affected_element=affected_element,
        )
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                InjectFaultLogEntry.tick == tick
                and InjectFaultLogEntry.schedule_blocked_fault_configuration
                == schedule_blocked_fault_configuration
                and InjectFaultLogEntry.affected_element == affected_element
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Schedule blocked fault with configuration {schedule_blocked_fault_configuration} "
            f"on element {affected_element}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.schedule_blocked_fault_configuration
            == schedule_blocked_fault_configuration
        )
        assert log_entry.affected_element == affected_element

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_train_prio_fault(
        self,
        run,
        tick,
        train_prio_fault_configuration,
        affected_element,
        value_before,
        value_after,
    ):
        logger = Logger(run_id=run.id)
        logger.inject_train_prio_fault(
            tick=tick,
            train_prio_fault_configuration=train_prio_fault_configuration,
            affected_element=affected_element,
            value_before=value_before,
            value_after=value_after,
        )
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                InjectFaultLogEntry.tick == tick
                and InjectFaultLogEntry.train_prio_fault_configuration
                == train_prio_fault_configuration
                and InjectFaultLogEntry.affected_element == affected_element
                and InjectFaultLogEntry.value_before == value_before
                and InjectFaultLogEntry.value_after == value_after
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train prio fault with configuration {train_prio_fault_configuration} "
            f"on element {affected_element} changed from {value_before} to {value_after}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.train_prio_fault_configuration == train_prio_fault_configuration
        )
        assert log_entry.affected_element == affected_element
        assert log_entry.value_before == value_before
        assert log_entry.value_after == value_after

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_train_speed_fault(
        self,
        run,
        tick,
        train_speed_fault_configuration,
        affected_element,
        value_before,
        value_after,
    ):
        logger = Logger(run_id=run.id)
        logger.inject_train_speed_fault(
            tick=tick,
            train_speed_fault_configuration=train_speed_fault_configuration,
            affected_element=affected_element,
            value_before=value_before,
            value_after=value_after,
        )
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                InjectFaultLogEntry.tick == tick
                and InjectFaultLogEntry.train_speed_fault_configuration
                == train_speed_fault_configuration
                and InjectFaultLogEntry.affected_element == affected_element
                and InjectFaultLogEntry.value_before == value_before
                and InjectFaultLogEntry.value_after == value_after
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train speed fault with configuration {train_speed_fault_configuration} "
            f"on element {affected_element} changed from {value_before} to {value_after}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.train_speed_fault_configuration == train_speed_fault_configuration
        )
        assert log_entry.affected_element == affected_element
        assert log_entry.value_before == value_before
        assert log_entry.value_after == value_after

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
