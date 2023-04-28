import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

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
    def _trains(self):
        return ["ice_1", "ice_2", "ice_3", "ice_4"]

    @pytest.fixture
    def _stations(self):
        return ["station_1", "station_2", "station_3"]

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
                ["station_1", 10, 20, "ice_1"],
                ["station_2", 30, 40, "ice_1"],
                ["station_3", 50, 60, "ice_1"],
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

    @pytest.fixture
    def _platform_blocked_fault_configuration(self):
        return PlatformBlockedFaultConfiguration.create(
            start_tick=10, end_tick=20, affected_element_id="station_1"
        )

    @pytest.fixture
    def _track_blocked_fault_configuration(self):
        return TrackBlockedFaultConfiguration.create(
            start_tick=10, end_tick=20, affected_element_id="section_1"
        )

    @pytest.fixture
    def _track_speed_limit_fault_configuration(self):
        return TrackSpeedLimitFaultConfiguration.create(
            start_tick=10,
            end_tick=20,
            affected_element_id="section_1",
            new_speed_limit=10,
        )

    @pytest.fixture
    def _schedule_blocked_fault_configuration(self):
        return ScheduleBlockedFaultConfiguration.create(
            start_tick=10, end_tick=20, affected_element_id="ice_1"
        )

    @pytest.fixture
    def _train_prio_fault_configuration(self):
        return TrainPrioFaultConfiguration.create(
            start_tick=10, end_tick=20, affected_element_id="ice_1", new_prio=1
        )

    @pytest.fixture
    def _train_speed_fault_configuration(self):
        return TrainSpeedFaultConfiguration.create(
            start_tick=10, end_tick=20, affected_element_id="ice_1", new_speed=10
        )

    @pytest.fixture
    def _faults_df(self):
        return pd.DataFrame(
            {
                "begin_tick": [10, 10, 10, 10, 10, 10],
                "fault_type": [
                    "platform_blocked",
                    "track_blocked",
                    "track_speed_limit",
                    "schedule_blocked",
                    "train_prio",
                    "train_speed",
                ],
                "fault_id": [None, None, None, None, None, None],
                "affected_element": [
                    "station_1",
                    "section_1",
                    "section_1",
                    "ice_1",
                    "ice_1",
                    "ice_1",
                ],
                "value_before": [None, None, "100", None, "2", "100"],
                "value_after": [None, None, "10", None, "1", "10"],
                "end_tick": [20, 20, 20, 20, 20, 20],
            }
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

    def setup_faults(
        self,
        logger: Logger,
        _platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
        _track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
        _track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        _schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        _train_prio_fault_configuration: TrainPrioFaultConfiguration,
        _train_speed_fault_configuration: TrainSpeedFaultConfiguration,
    ):
        logger.inject_platform_blocked_fault(
            10, _platform_blocked_fault_configuration, "station_1"
        )
        logger.resolve_platform_blocked_fault(20, _platform_blocked_fault_configuration)

        logger.inject_track_blocked_fault(
            10, _track_blocked_fault_configuration, "section_1"
        )
        logger.resolve_track_blocked_fault(20, _track_blocked_fault_configuration)

        logger.inject_track_speed_limit_fault(
            10, _track_speed_limit_fault_configuration, "section_1", "100", "10"
        )
        logger.resolve_track_speed_limit_fault(
            20, _track_speed_limit_fault_configuration
        )

        logger.inject_schedule_blocked_fault(
            10, _schedule_blocked_fault_configuration, "ice_1"
        )
        logger.resolve_schedule_blocked_fault(20, _schedule_blocked_fault_configuration)

        logger.inject_train_prio_fault(
            10, _train_prio_fault_configuration, "ice_1", "2", "1"
        )
        logger.resolve_train_prio_fault(20, _train_prio_fault_configuration)

        logger.inject_train_speed_fault(
            10, _train_speed_fault_configuration, "ice_1", "100", "10"
        )
        logger.resolve_train_speed_fault(20, _train_speed_fault_configuration)

    def test_get_trains(self, _trains, logger, log_collector: LogCollector):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        trains = log_collector.get_trains()
        trains = sorted(trains)
        assert trains == _trains

    def test_get_stations(self, _stations, logger, log_collector: LogCollector):
        self.setup_departure_arrival_1(logger)
        self.setup_departure_arrival_2(logger)
        self.setup_departure_arrival_3(logger)
        self.setup_departure_arrival_4(logger)
        stations = log_collector.get_stations()
        stations = sorted(stations)
        assert stations == _stations

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

    def test_departure_arrival__multiple_runs(
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

    def test_get_faults(
        self,
        _faults_df,
        logger,
        _platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
        _track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
        _track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        _schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        _train_prio_fault_configuration: TrainPrioFaultConfiguration,
        _train_speed_fault_configuration: TrainSpeedFaultConfiguration,
        log_collector: LogCollector,
    ):
        self.setup_faults(
            logger,
            _platform_blocked_fault_configuration,
            _track_blocked_fault_configuration,
            _track_speed_limit_fault_configuration,
            _schedule_blocked_fault_configuration,
            _train_prio_fault_configuration,
            _train_speed_fault_configuration,
        )
        _faults_df["fault_id"] = [
            _platform_blocked_fault_configuration.id,
            _track_blocked_fault_configuration.id,
            _track_speed_limit_fault_configuration.id,
            _schedule_blocked_fault_configuration.id,
            _train_prio_fault_configuration.id,
            _train_speed_fault_configuration.id,
        ]
        _faults_df["fault_id"] = _faults_df["fault_id"].astype("string")
        faults_df = log_collector.get_faults(logger.run_id)
        assert_frame_equal(faults_df, _faults_df)
