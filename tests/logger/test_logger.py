from datetime import datetime

from freezegun import freeze_time

from src.logger.log_entry import TrainSpawnLogEntry
from src.logger.logger import Logger


class TestLogger:
    """Class for testing logger functions."""

    @freeze_time()
    def test_spawn_train(self, run, train_id):
        logger = Logger(run_id=run.id)
        logger.spawn_train(train_id=train_id)
        log_entry = (
            TrainSpawnLogEntry.select()
            .where(TrainSpawnLogEntry.train_id == train_id)
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.message == f"Train with ID {train_id} spawned"
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
