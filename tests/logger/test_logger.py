from datetime import datetime

from freezegun import freeze_time

from src.logger.log_entry import (
    TrainArrivalLogEntry,
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
            .where(TrainArrivalLogEntry.train_id == train_id)
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
