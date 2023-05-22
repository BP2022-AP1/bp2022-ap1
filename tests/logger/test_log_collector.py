import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.implementor.models import Run
from src.logger.log_collector import LogCollector
from src.logger.logger import Logger
from tests.decorators import recreate_db_setup


# pylint: disable=too-many-public-methods
class TestLogCollector:
    """Tests for the LogCollector class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def _run_ids(self, run: Run):
        return [run.id]

    @pytest.fixture
    def _config_ids(self, simulation_configuration):
        return [simulation_configuration.id]

    @pytest.fixture
    def _departure_arrival_1_df(self):
        departure_arrival_df = pd.DataFrame(
            [["station_1", 10, 20], ["station_2", 30, 40], ["station_3", 50, 60]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )
        departure_arrival_df["arrival_tick"] = departure_arrival_df[
            "arrival_tick"
        ].astype("Int64")
        departure_arrival_df["departure_tick"] = departure_arrival_df[
            "departure_tick"
        ].astype("Int64")
        return departure_arrival_df

    @pytest.fixture
    def _departure_arrival_all_1_df(self):
        departure_arrival_df = pd.DataFrame(
            [
                ["station_1", 10, 20, "ice_1_passenger"],
                ["station_2", 30, 40, "ice_1_passenger"],
                ["station_3", 50, 60, "ice_1_passenger"],
            ],
            columns=["station_id", "arrival_tick", "departure_tick", "train_id"],
        )
        departure_arrival_df["arrival_tick"] = departure_arrival_df[
            "arrival_tick"
        ].astype("Int64")
        departure_arrival_df["departure_tick"] = departure_arrival_df[
            "departure_tick"
        ].astype("Int64")
        return departure_arrival_df

    @pytest.fixture
    def _departure_arrival_2_df(self):
        departure_arrival_df = pd.DataFrame(
            [["station_1", 10, 20], ["station_2", 30, 40], ["station_3", 50, None]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )
        departure_arrival_df["arrival_tick"] = departure_arrival_df[
            "arrival_tick"
        ].astype("Int64")
        departure_arrival_df["departure_tick"] = departure_arrival_df[
            "departure_tick"
        ].astype("Int64")
        return departure_arrival_df

    @pytest.fixture
    def _departure_arrival_3_df(self):
        departure_arrival_df = pd.DataFrame(
            [["station_1", None, 20], ["station_2", 30, 40], ["station_3", 50, 60]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )
        departure_arrival_df["arrival_tick"] = departure_arrival_df[
            "arrival_tick"
        ].astype("Int64")
        departure_arrival_df["departure_tick"] = departure_arrival_df[
            "departure_tick"
        ].astype("Int64")
        return departure_arrival_df

    @pytest.fixture
    def _departure_arrival_4_df(self):
        departure_arrival_df = pd.DataFrame(
            [["station_1", None, 20], ["station_2", 30, 40], ["station_3", 50, None]],
            columns=["station_id", "arrival_tick", "departure_tick"],
        )
        departure_arrival_df["arrival_tick"] = departure_arrival_df[
            "arrival_tick"
        ].astype("Int64")
        departure_arrival_df["departure_tick"] = departure_arrival_df[
            "departure_tick"
        ].astype("Int64")
        return departure_arrival_df

    @pytest.fixture
    def _departure_arrival_all_df(self):
        departure_arrival_df = pd.DataFrame(
            [
                ["station_1", None, 20, "cargo_4_cargo"],
                ["station_2", 30, 40, "cargo_4_cargo"],
                ["station_3", 50, None, "cargo_4_cargo"],
                ["station_1", 10, 20, "ice_1_passenger"],
                ["station_2", 30, 40, "ice_1_passenger"],
                ["station_3", 50, 60, "ice_1_passenger"],
                ["station_1", 10, 20, "ice_2_passenger"],
                ["station_2", 30, 40, "ice_2_passenger"],
                ["station_3", 50, None, "ice_2_passenger"],
                ["station_1", None, 20, "ice_3_passenger"],
                ["station_2", 30, 40, "ice_3_passenger"],
                ["station_3", 50, 60, "ice_3_passenger"],
            ],
            columns=["station_id", "arrival_tick", "departure_tick", "train_id"],
        )
        departure_arrival_df["arrival_tick"] = departure_arrival_df[
            "arrival_tick"
        ].astype("Int64")
        departure_arrival_df["departure_tick"] = departure_arrival_df[
            "departure_tick"
        ].astype("Int64")
        return departure_arrival_df

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
                [None, 20, "section_1", None],
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
                [None, 20, "section_1", None],
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
                [None, 20, "section_1", None, "cargo_4_cargo"],
                [30, 40, "section_2", 20.5, "cargo_4_cargo"],
                [50, None, "section_3", 30.5, "cargo_4_cargo"],
                [10, 20, "section_1", 10.5, "ice_1_passenger"],
                [30, 40, "section_2", 20.5, "ice_1_passenger"],
                [50, 60, "section_3", 30.5, "ice_1_passenger"],
                [10, 20, "section_1", 10.5, "ice_2_passenger"],
                [30, 40, "section_2", 20.5, "ice_2_passenger"],
                [50, None, "section_3", 30.5, "ice_2_passenger"],
                [None, 20, "section_1", None, "ice_3_passenger"],
                [30, 40, "section_2", 20.5, "ice_3_passenger"],
                [50, 60, "section_3", 30.5, "ice_3_passenger"],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
                "train_id",
            ],
        )

    @staticmethod
    def setup_departure_arrival_1(logger):
        logger.arrival_train(10, "ice_1_passenger", "station_1")
        logger.departure_train(20, "ice_1_passenger", "station_1")
        logger.arrival_train(30, "ice_1_passenger", "station_2")
        logger.departure_train(40, "ice_1_passenger", "station_2")
        logger.arrival_train(50, "ice_1_passenger", "station_3")
        logger.departure_train(60, "ice_1_passenger", "station_3")

    @staticmethod
    def setup_departure_arrival_2(logger):
        logger.arrival_train(10, "ice_2_passenger", "station_1")
        logger.departure_train(20, "ice_2_passenger", "station_1")
        logger.arrival_train(30, "ice_2_passenger", "station_2")
        logger.departure_train(40, "ice_2_passenger", "station_2")
        logger.arrival_train(50, "ice_2_passenger", "station_3")

    @staticmethod
    def setup_departure_arrival_3(logger):
        logger.departure_train(20, "ice_3_passenger", "station_1")
        logger.arrival_train(30, "ice_3_passenger", "station_2")
        logger.departure_train(40, "ice_3_passenger", "station_2")
        logger.arrival_train(50, "ice_3_passenger", "station_3")
        logger.departure_train(60, "ice_3_passenger", "station_3")

    @staticmethod
    def setup_departure_arrival_4(logger):
        logger.departure_train(20, "cargo_4_cargo", "station_1")
        logger.arrival_train(30, "cargo_4_cargo", "station_2")
        logger.departure_train(40, "cargo_4_cargo", "station_2")
        logger.arrival_train(50, "cargo_4_cargo", "station_3")

    @staticmethod
    def setup_departure_arrival_1_alt(logger):
        logger.arrival_train(20, "ice_1_passenger", "station_1")
        logger.departure_train(30, "ice_1_passenger", "station_1")
        logger.arrival_train(40, "ice_1_passenger", "station_2")
        logger.departure_train(50, "ice_1_passenger", "station_2")
        logger.arrival_train(60, "ice_1_passenger", "station_3")
        logger.departure_train(70, "ice_1_passenger", "station_3")

    @staticmethod
    def setup_departure_arrival_2_alt(logger):
        logger.arrival_train(20, "ice_2_passenger", "station_1")
        logger.departure_train(30, "ice_2_passenger", "station_1")
        logger.arrival_train(40, "ice_2_passenger", "station_2")
        logger.departure_train(50, "ice_2_passenger", "station_2")
        logger.arrival_train(60, "ice_2_passenger", "station_3")

    @staticmethod
    def setup_departure_arrival_3_alt(logger):
        logger.departure_train(30, "ice_3_passenger", "station_1")
        logger.arrival_train(40, "ice_3_passenger", "station_2")
        logger.departure_train(50, "ice_3_passenger", "station_2")
        logger.arrival_train(60, "ice_3_passenger", "station_3")
        logger.departure_train(70, "ice_3_passenger", "station_3")

    @staticmethod
    def setup_departure_arrival_4_alt(logger):
        logger.departure_train(30, "cargo_4_cargo", "station_1")
        logger.arrival_train(40, "cargo_4_cargo", "station_2")
        logger.departure_train(50, "cargo_4_cargo", "station_2")
        logger.arrival_train(60, "cargo_4_cargo", "station_3")

    @staticmethod
    def setup_enter_leave_block_section_1(logger):
        logger.train_enter_block_section(10, "ice_1_passenger", "section_1", 10.5)
        logger.train_leave_block_section(20, "ice_1_passenger", "section_1")
        logger.train_enter_block_section(30, "ice_1_passenger", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_1_passenger", "section_2")
        logger.train_enter_block_section(50, "ice_1_passenger", "section_3", 30.5)
        logger.train_leave_block_section(60, "ice_1_passenger", "section_3")

    @staticmethod
    def setup_enter_leave_block_section_2(logger):
        logger.train_enter_block_section(10, "ice_2_passenger", "section_1", 10.5)
        logger.train_leave_block_section(20, "ice_2_passenger", "section_1")
        logger.train_enter_block_section(30, "ice_2_passenger", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_2_passenger", "section_2")
        logger.train_enter_block_section(50, "ice_2_passenger", "section_3", 30.5)

    @staticmethod
    def setup_enter_leave_block_section_3(logger):
        logger.train_leave_block_section(20, "ice_3_passenger", "section_1")
        logger.train_enter_block_section(30, "ice_3_passenger", "section_2", 20.5)
        logger.train_leave_block_section(40, "ice_3_passenger", "section_2")
        logger.train_enter_block_section(50, "ice_3_passenger", "section_3", 30.5)
        logger.train_leave_block_section(60, "ice_3_passenger", "section_3")

    @staticmethod
    def setup_enter_leave_block_section_4(logger):
        logger.train_leave_block_section(20, "cargo_4_cargo", "section_1")
        logger.train_enter_block_section(30, "cargo_4_cargo", "section_2", 20.5)
        logger.train_leave_block_section(40, "cargo_4_cargo", "section_2")
        logger.train_enter_block_section(50, "cargo_4_cargo", "section_3", 30.5)

    @staticmethod
    def setup_logs_spawn_trains(logger):
        logger.spawn_train(4600, "Kohlezug 1")
        logger.spawn_train(7300, "Kohlezug 2")
        logger.spawn_train(10900, "Kohlezug 3")
        logger.spawn_train(13600, "Kohlezug 4")
        logger.spawn_train(17200, "Kohlezug 5")

    @staticmethod
    def setup_faults(
        logger: Logger,
        platform_blocked_fault_configuration,
        track_blocked_fault_configuration,
        track_speed_limit_fault_configuration,
        schedule_blocked_fault_configuration,
        train_prio_fault_configuration,
        train_speed_fault_configuration,
    ):
        logger.inject_platform_blocked_fault(
            10, platform_blocked_fault_configuration, "station_1"
        )
        logger.resolve_platform_blocked_fault(20, platform_blocked_fault_configuration)

        logger.inject_track_blocked_fault(
            10, track_blocked_fault_configuration, "section_1"
        )
        logger.resolve_track_blocked_fault(20, track_blocked_fault_configuration)

        logger.inject_track_speed_limit_fault(
            10, track_speed_limit_fault_configuration, "section_1", "100", "10"
        )
        logger.resolve_track_speed_limit_fault(
            20, track_speed_limit_fault_configuration
        )

        logger.inject_schedule_blocked_fault(
            10, schedule_blocked_fault_configuration, "ice_1_passenger"
        )
        logger.resolve_schedule_blocked_fault(20, schedule_blocked_fault_configuration)

        logger.inject_train_prio_fault(
            10, train_prio_fault_configuration, "ice_1_passenger", "2", "1"
        )
        logger.resolve_train_prio_fault(20, train_prio_fault_configuration)

        logger.inject_train_speed_fault(
            10, train_speed_fault_configuration, "ice_1_passenger", "100", "10"
        )
        logger.resolve_train_speed_fault(20, train_speed_fault_configuration)

    def test_get_trains(self, trains, logger, log_collector: LogCollector):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        _trains = log_collector.get_trains()
        _trains = sorted(_trains)
        assert _trains == trains

    def test_get_stations(self, stations, logger, log_collector: LogCollector):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        _stations = log_collector.get_stations()
        _stations = sorted(_stations)
        assert _stations == stations

    def test_get_run_ids(self, _run_ids, logger, log_collector: LogCollector):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        run_ids = log_collector.get_run_ids()
        run_ids = sorted(run_ids)
        assert run_ids == _run_ids

    def test_get_simulation_config_ids(
        self, _config_ids, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        simulation_config_ids = log_collector.get_config_ids()
        simulation_config_ids = sorted(simulation_config_ids)
        assert simulation_config_ids == _config_ids

    def test_departure_arrival_1(
        self, _departure_arrival_1_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                logger.run_id, "ice_1_passenger"
            ),
            _departure_arrival_1_df,
        )

    def test_departure_arrival_2(
        self, _departure_arrival_2_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_2(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                logger.run_id, "ice_2_passenger"
            ),
            _departure_arrival_2_df,
        )

    def test_departure_arrival_3(
        self, _departure_arrival_3_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_3(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                logger.run_id, "ice_3_passenger"
            ),
            _departure_arrival_3_df,
        )

    def test_departure_arrival_4(
        self, _departure_arrival_4_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_4(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                logger.run_id, "cargo_4_cargo"
            ),
            _departure_arrival_4_df,
        )

    def test_enter_leave_block_section_1(
        self, _enter_leave_block_section_1_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_1(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(
                logger.run_id, "ice_1_passenger"
            ),
            _enter_leave_block_section_1_df,
        )

    def test_enter_leave_block_section_2(
        self, _enter_leave_block_section_2_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_2(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(
                logger.run_id, "ice_2_passenger"
            ),
            _enter_leave_block_section_2_df,
        )

    def test_enter_leave_block_section_3(
        self, _enter_leave_block_section_3_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_3(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(
                logger.run_id, "ice_3_passenger"
            ),
            _enter_leave_block_section_3_df,
        )

    def test_enter_leave_block_section_4(
        self, _enter_leave_block_section_4_df, logger, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_4(logger)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(
                logger.run_id, "cargo_4_cargo"
            ),
            _enter_leave_block_section_4_df,
        )

    def test_departure_arrival_all(
        self, _departure_arrival_all_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(logger.run_id),
            _departure_arrival_all_df,
        )

    def test_departure_arrival_all_1(
        self, _departure_arrival_all_1_df, logger, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(logger)
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(logger.run_id),
            _departure_arrival_all_1_df,
        )

    def test_departure_arrival_empty(self, logger: Logger, log_collector: LogCollector):
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(logger.run_id),
            pd.DataFrame(
                columns=["train_id", "station_id", "arrival_tick", "departure_tick"]
            ),
        )

    def test_departure_arrival_multiple_runs(
        self,
        logger: Logger,
        logger2: Logger,
        log_collector: LogCollector,
        _departure_arrival_all_df,
    ):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        self.setup_departure_arrival_1(logger2)
        self.setup_departure_arrival_2(logger2)
        self.setup_departure_arrival_3(logger2)
        self.setup_departure_arrival_4(logger2)

        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(logger.run_id),
            _departure_arrival_all_df,
        )
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(logger2.run_id),
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

    def test_get_train_spawn_times(
        self,
        train_spawn_times_df: pd.DataFrame,
        logger: Logger,
        log_collector: LogCollector,
    ):
        self.setup_logs_spawn_trains(logger)
        assert_frame_equal(
            train_spawn_times_df, log_collector.get_train_spawn_times(logger.run_id)
        )

    def test_get_faults(
        self,
        faults_log_collector_df,
        logger,
        platform_blocked_fault_configuration,
        track_blocked_fault_configuration,
        track_speed_limit_fault_configuration,
        schedule_blocked_fault_configuration,
        train_prio_fault_configuration,
        train_speed_fault_configuration,
        log_collector: LogCollector,
    ):
        # pylint: disable=duplicate-code
        self.setup_faults(
            logger,
            platform_blocked_fault_configuration,
            track_blocked_fault_configuration,
            track_speed_limit_fault_configuration,
            schedule_blocked_fault_configuration,
            train_prio_fault_configuration,
            train_speed_fault_configuration,
        )
        faults_log_collector_df["fault_id"] = faults_log_collector_df[
            "fault_id"
        ].astype("string")
        generated_faults_df = log_collector.get_faults(logger.run_id)
        assert_frame_equal(generated_faults_df, faults_log_collector_df)
