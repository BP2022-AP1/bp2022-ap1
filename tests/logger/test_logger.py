from datetime import datetime

from freezegun import freeze_time

from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
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
