import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.logger.log_collector import LogCollector
from tests.decorators import recreate_db_setup


class TestLogCollector:
    """Tests for the LogCollector class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def _departure_arrival_1_df(self):
        return pd.DataFrame(
            [["station_1", 10, 20], ["station_2", 30, 40], ["station_3", 50, 60]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )

    @pytest.fixture
    def _departure_arrival_2_df(self):
        return pd.DataFrame(
            [["station_1", 10, 20], ["station_2", 30, 40], ["station_3", 50, None]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )

    @pytest.fixture
    def _departure_arrival_3_df(self):
        return pd.DataFrame(
            [["station_1", None, 20], ["station_2", 30, 40], ["station_3", 50, 60]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )

    @pytest.fixture
    def _departure_arrival_4_df(self):
        return pd.DataFrame(
            [["station_1", None, 20], ["station_2", 30, 40], ["station_3", 50, None]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )

    @pytest.fixture
    def _departure_arrival_all_df(self):
        return pd.DataFrame(
            [
                ["station_1", 10, 20, "ice_1"],
                ["station_2", 30, 40, "ice_1"],
                ["station_3", 50, 60, "ice_1"],
                ["station_1", 10, 20, "ice_2"],
                ["station_2", 30, 40, "ice_2"],
                ["station_3", 50, None, "ice_2"],
                ["station_1", None, 20, "ice_3"],
                ["station_2", 30, 40, "ice_3"],
                ["station_3", 50, 60, "ice_3"],
                ["station_1", None, 20, "ice_4"],
                ["station_2", 30, 40, "ice_4"],
                ["station_3", 50, None, "ice_4"],
            ],
            columns=["station_id", "arrival_tick", "departure_tick", "train_id"],
        )

    @pytest.fixture
    def _enter_leave_block_section_1_df(self):
        return pd.DataFrame(
            [
                [10, 20, "section_1", 10.5],
                [30, 40, "section_2", 20.5],
                [50, 60, "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_block_section_2_df(self):
        return pd.DataFrame(
            [
                [10, 20, "section_1", 10.5],
                [30, 40, "section_2", 20.5],
                [50, None, "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_block_section_3_df(self):
        return pd.DataFrame(
            [
                [None, 20, "section_1", 10.5],
                [30, 40, "section_2", 20.5],
                [50, 60, "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_block_section_4_df(self):
        return pd.DataFrame(
            [
                [None, 20, "section_1", 10.5],
                [30, 40, "section_2", 20.5],
                [50, None, "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_block_section_all_df(self):
        return pd.DataFrame(
            [
                [10, 20, "section_1", 10.5, "ice_1"],
                [30, 40, "section_2", 20.5, "ice_1"],
                [50, 60, "section_3", 30.5, "ice_1"],
                [10, 20, "section_1", 10.5, "ice_2"],
                [30, 40, "section_2", 20.5, "ice_2"],
                [50, None, "section_3", 30.5, "ice_2"],
                [None, 20, "section_1", 10.5, "ice_3"],
                [30, 40, "section_2", 20.5, "ice_3"],
                [50, 60, "section_3", 30.5, "ice_3"],
                [None, 20, "section_1", 10.5, "ice_4"],
                [30, 40, "section_2", 20.5, "ice_4"],
                [50, None, "section_3", 30.5, "ice_4"],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
                "train_id",
            ],
        )

    def setup_departure_arrival_1(self, logger):
        logger.arrival_train(10, "ice_1", "station_1")
        logger.departure_train(20, "ice_1", "station_1")
        logger.arrival_train(30, "ice_1", "station_2")
        logger.departure_train(40, "ice_1", "station_2")
        logger.arrival_train(50, "ice_1", "station_3")
        logger.departure_train(60, "ice_1", "station_3")

    def setup_departure_arrival_2(self, logger):
        logger.arrival_train(10, "ice_2", "station_1")
        logger.departure_train(20, "ice_2", "station_1")
        logger.arrival_train(30, "ice_2", "station_2")
        logger.departure_train(40, "ice_2", "station_2")
        logger.arrival_train(50, "ice_2", "station_3")

    def setup_departure_arrival_3(self, logger):
        logger.departure_train(20, "ice_3", "station_1")
        logger.arrival_train(30, "ice_3", "station_2")
        logger.departure_train(40, "ice_3", "station_2")
        logger.arrival_train(50, "ice_3", "station_3")
        logger.departure_train(60, "ice_3", "station_3")

    def setup_departure_arrival_4(self, logger):
        logger.departure_train(20, "ice_4", "station_1")
        logger.arrival_train(30, "ice_4", "station_2")
        logger.departure_train(40, "ice_4", "station_2")
        logger.arrival_train(50, "ice_4", "station_3")

    def setup_enter_leave_block_section_1(self, logger):
        logger.train_enter_block_section(10, "ice_1", "section_1", 10.5)
        logger.train_leave_block_section(20, "ice_1", "section_1", 10.5)
        logger.train_enter_block_section(30, "ice_1", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_1", "section_2", 20.5)
        logger.train_enter_block_section(50, "ice_1", "section_3", 30.5)
        logger.train_leave_block_section(60, "ice_1", "section_3", 30.5)

    def setup_enter_leave_block_section_2(self, logger):
        logger.train_enter_block_section(10, "ice_2", "section_1", 10.5)
        logger.train_leave_block_section(20, "ice_2", "section_1", 10.5)
        logger.train_enter_block_section(30, "ice_2", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_2", "section_2", 20.5)
        logger.train_enter_block_section(50, "ice_2", "section_3", 30.5)

    def setup_enter_leave_block_section_3(self, logger):
        logger.train_leave_block_section(20, "ice_3", "section_1", 10.5)
        logger.train_enter_block_section(30, "ice_3", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_3", "section_2", 20.5)
        logger.train_enter_block_section(50, "ice_3", "section_3", 30.5)
        logger.train_leave_block_section(60, "ice_3", "section_3", 30.5)

    def setup_enter_leave_block_section_4(self, logger):
        logger.train_leave_block_section(20, "ice_4", "section_1", 10.5)
        logger.train_enter_block_section(30, "ice_4", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_4", "section_2", 20.5)
        logger.train_enter_block_section(50, "ice_4", "section_3", 30.5)

    def test_departure_arrival_1(
        self, _departure_arrival_1_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(logger.run_id, "ice_1"),
            _departure_arrival_1_df,
        )

    def test_departure_arrival_2(
        self, _departure_arrival_2_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_2(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(logger.run_id, "ice_2"),
            _departure_arrival_2_df,
        )

    def test_departure_arrival_3(
        self, _departure_arrival_3_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_3(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(logger.run_id, "ice_3"),
            _departure_arrival_3_df,
        )

    def test_departure_arrival_4(
        self, _departure_arrival_4_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_4(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(logger.run_id, "ice_4"),
            _departure_arrival_4_df,
        )

    def test_enter_leave_block_section_1(
        self, _enter_leave_block_section_1_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_1(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(logger.run_id, "ice_1"),
            _enter_leave_block_section_1_df,
        )

    def test_enter_leave_block_section_2(
        self, _enter_leave_block_section_2_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_2(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(logger.run_id, "ice_2"),
            _enter_leave_block_section_2_df,
        )

    def test_enter_leave_block_section_3(
        self, _enter_leave_block_section_3_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_3(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(logger.run_id, "ice_3"),
            _enter_leave_block_section_3_df,
        )

    def test_enter_leave_block_section_4(
        self, _enter_leave_block_section_4_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_4(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(logger.run_id, "ice_4"),
            _enter_leave_block_section_4_df,
        )

    def test_departure_arrival_all(
        self, _departure_arrival_all_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        print("one", _departure_arrival_all_df)
        print("two", log_collector.get_departures_arrivals_all_trains(logger.run_id))
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(logger.run_id),
            _departure_arrival_all_df,
        )

    def test_enter_leave_block_section_all(
        self, _enter_leave_block_section_all_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_1(logger)
        self.setup_enter_leave_block_section_2(logger)
        self.setup_enter_leave_block_section_3(logger)
        self.setup_enter_leave_block_section_4(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_all_trains(logger.run_id),
            _enter_leave_block_section_all_df,
        )
