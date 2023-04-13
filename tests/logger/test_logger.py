from datetime import datetime

from freezegun import freeze_time

from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    RemoveFahrstrasseLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)
from src.logger.logger import Logger


class TestLogger:
    """Class for testing logger functions."""

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
