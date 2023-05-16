import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.event_bus.event import Event, EventType
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
                [10, 20, "section_1", 10.5, "ice_1"],
                [30, 40, "section_2", 20.5, "ice_1"],
                [50, 60, "section_3", 30.5, "ice_1"],
                [10, 20, "section_1", 10.5, "ice_2"],
                [30, 40, "section_2", 20.5, "ice_2"],
                [50, None, "section_3", 30.5, "ice_2"],
                [None, 20, "section_1", None, "ice_3"],
                [30, 40, "section_2", 20.5, "ice_3"],
                [50, 60, "section_3", 30.5, "ice_3"],
                [None, 20, "section_1", None, "ice_4"],
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

    @staticmethod
    def setup_departure_arrival_1(event_bus):
        event_bus.arrival_train(10, "ice_1", "station_1")
        event_bus.departure_train(20, "ice_1", "station_1")
        event_bus.arrival_train(30, "ice_1", "station_2")
        event_bus.departure_train(40, "ice_1", "station_2")
        event_bus.arrival_train(50, "ice_1", "station_3")
        event_bus.departure_train(60, "ice_1", "station_3")

    @staticmethod
    def setup_departure_arrival_2(event_bus):
        event_bus.arrival_train(10, "ice_2", "station_1")
        event_bus.departure_train(20, "ice_2", "station_1")
        event_bus.arrival_train(30, "ice_2", "station_2")
        event_bus.departure_train(40, "ice_2", "station_2")
        event_bus.arrival_train(50, "ice_2", "station_3")

    @staticmethod
    def setup_departure_arrival_3(event_bus):
        event_bus.departure_train(20, "ice_3", "station_1")
        event_bus.arrival_train(30, "ice_3", "station_2")
        event_bus.departure_train(40, "ice_3", "station_2")
        event_bus.arrival_train(50, "ice_3", "station_3")
        event_bus.departure_train(60, "ice_3", "station_3")

    @staticmethod
    def setup_departure_arrival_4(event_bus):
        event_bus.departure_train(20, "ice_4", "station_1")
        event_bus.arrival_train(30, "ice_4", "station_2")
        event_bus.departure_train(40, "ice_4", "station_2")
        event_bus.arrival_train(50, "ice_4", "station_3")

    @staticmethod
    def setup_departure_arrival_1_alt(event_bus):
        event_bus.arrival_train(20, "ice_1", "station_1")
        event_bus.departure_train(30, "ice_1", "station_1")
        event_bus.arrival_train(40, "ice_1", "station_2")
        event_bus.departure_train(50, "ice_1", "station_2")
        event_bus.arrival_train(60, "ice_1", "station_3")
        event_bus.departure_train(70, "ice_1", "station_3")

    @staticmethod
    def setup_departure_arrival_2_alt(event_bus):
        event_bus.arrival_train(20, "ice_2", "station_1")
        event_bus.departure_train(30, "ice_2", "station_1")
        event_bus.arrival_train(40, "ice_2", "station_2")
        event_bus.departure_train(50, "ice_2", "station_2")
        event_bus.arrival_train(60, "ice_2", "station_3")

    @staticmethod
    def setup_departure_arrival_3_alt(event_bus):
        event_bus.departure_train(30, "ice_3", "station_1")
        event_bus.arrival_train(40, "ice_3", "station_2")
        event_bus.departure_train(50, "ice_3", "station_2")
        event_bus.arrival_train(60, "ice_3", "station_3")
        event_bus.departure_train(70, "ice_3", "station_3")

    @staticmethod
    def setup_departure_arrival_4_alt(event_bus):
        event_bus.departure_train(30, "ice_4", "station_1")
        event_bus.arrival_train(40, "ice_4", "station_2")
        event_bus.departure_train(50, "ice_4", "station_2")
        event_bus.arrival_train(60, "ice_4", "station_3")

    @staticmethod
    def setup_enter_leave_block_section_1(event_bus):
        event_bus.train_enter_block_section(10, "ice_1", "section_1", 10.5)
        event_bus.train_leave_block_section(20, "ice_1", "section_1", 10.5)
        event_bus.train_enter_block_section(30, "ice_1", "section_2", 20.5)
        event_bus.train_leave_block_section(40, "ice_1", "section_2", 20.5)
        event_bus.train_enter_block_section(50, "ice_1", "section_3", 30.5)
        event_bus.train_leave_block_section(60, "ice_1", "section_3", 30.5)

    @staticmethod
    def setup_enter_leave_block_section_2(event_bus):
        event_bus.train_enter_block_section(10, "ice_2", "section_1", 10.5)
        event_bus.train_leave_block_section(20, "ice_2", "section_1", 10.5)
        event_bus.train_enter_block_section(30, "ice_2", "section_2", 20.5)
        event_bus.train_leave_block_section(40, "ice_2", "section_2", 20.5)
        event_bus.train_enter_block_section(50, "ice_2", "section_3", 30.5)

    @staticmethod
    def setup_enter_leave_block_section_3(event_bus):
        event_bus.train_leave_block_section(20, "ice_3", "section_1", 10.5)
        event_bus.train_enter_block_section(30, "ice_3", "section_2", 20.5)
        event_bus.train_leave_block_section(40, "ice_3", "section_2", 20.5)
        event_bus.train_enter_block_section(50, "ice_3", "section_3", 30.5)
        event_bus.train_leave_block_section(60, "ice_3", "section_3", 30.5)

    @staticmethod
    def setup_enter_leave_block_section_4(event_bus):
        event_bus.train_leave_block_section(20, "ice_4", "section_1", 10.5)
        event_bus.train_enter_block_section(30, "ice_4", "section_2", 20.5)
        event_bus.train_leave_block_section(40, "ice_4", "section_2", 20.5)
        event_bus.train_enter_block_section(50, "ice_4", "section_3", 30.5)

    @staticmethod
    def setup_logs_spawn_trains(event_bus):
        event_bus.spawn_train(4600, "Kohlezug 1")
        event_bus.spawn_train(7300, "Kohlezug 2")
        event_bus.spawn_train(10900, "Kohlezug 3")
        event_bus.spawn_train(13600, "Kohlezug 4")
        event_bus.spawn_train(17200, "Kohlezug 5")

    @staticmethod
    def setup_faults(
        event_bus: Logger,
        platform_blocked_fault_configuration,
        track_blocked_fault_configuration,
        track_speed_limit_fault_configuration,
        schedule_blocked_fault_configuration,
        train_prio_fault_configuration,
        train_speed_fault_configuration,
    ):
        event_bus.inject_platform_blocked_fault(
            10, platform_blocked_fault_configuration, "station_1"
        )
        event_bus.resolve_platform_blocked_fault(
            20, platform_blocked_fault_configuration
        )

        event_bus.inject_track_blocked_fault(
            10, track_blocked_fault_configuration, "section_1"
        )
        event_bus.resolve_track_blocked_fault(20, track_blocked_fault_configuration)

        event_bus.inject_track_speed_limit_fault(
            10, track_speed_limit_fault_configuration, "section_1", "100", "10"
        )
        event_bus.resolve_track_speed_limit_fault(
            20, track_speed_limit_fault_configuration
        )

        event_bus.inject_schedule_blocked_fault(
            10, schedule_blocked_fault_configuration, "ice_1"
        )
        event_bus.resolve_schedule_blocked_fault(
            20, schedule_blocked_fault_configuration
        )

        event_bus.inject_train_prio_fault(
            10, train_prio_fault_configuration, "ice_1", "2", "1"
        )
        event_bus.resolve_train_prio_fault(20, train_prio_fault_configuration)

        event_bus.inject_train_speed_fault(
            10, train_speed_fault_configuration, "ice_1", "100", "10"
        )
        event_bus.resolve_train_speed_fault(20, train_speed_fault_configuration)

    def test_get_trains(self, _trains, event_bus, log_collector: LogCollector):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        trains = log_collector.get_trains()
        trains = sorted(trains)
        assert trains == _trains

    def test_get_stations(self, _stations, event_bus, log_collector: LogCollector):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        stations = log_collector.get_stations()
        stations = sorted(stations)
        assert stations == _stations

    def test_get_run_ids(self, _run_ids, event_bus, log_collector: LogCollector):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        run_ids = log_collector.get_run_ids()
        run_ids = sorted(run_ids)
        assert run_ids == _run_ids

    def test_get_simulation_config_ids(
        self, _config_ids, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        simulation_config_ids = log_collector.get_config_ids()
        simulation_config_ids = sorted(simulation_config_ids)
        assert simulation_config_ids == _config_ids

    def test_departure_arrival_1(
        self, _departure_arrival_1_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(event_bus.run_id, "ice_1"),
            _departure_arrival_1_df,
        )

    def test_departure_arrival_2(
        self, _departure_arrival_2_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_2(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(event_bus.run_id, "ice_2"),
            _departure_arrival_2_df,
        )

    def test_departure_arrival_3(
        self, _departure_arrival_3_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_3(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(event_bus.run_id, "ice_3"),
            _departure_arrival_3_df,
        )

    def test_departure_arrival_4(
        self, _departure_arrival_4_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_4(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(event_bus.run_id, "ice_4"),
            _departure_arrival_4_df,
        )

    def test_enter_leave_block_section_1(
        self, _enter_leave_block_section_1_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_1(event_bus)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(event_bus.run_id, "ice_1"),
            _enter_leave_block_section_1_df,
        )

    def test_enter_leave_block_section_2(
        self, _enter_leave_block_section_2_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_2(event_bus)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(event_bus.run_id, "ice_2"),
            _enter_leave_block_section_2_df,
        )

    def test_enter_leave_block_section_3(
        self, _enter_leave_block_section_3_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_3(event_bus)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(event_bus.run_id, "ice_3"),
            _enter_leave_block_section_3_df,
        )

    def test_enter_leave_block_section_4(
        self, _enter_leave_block_section_4_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_4(event_bus)
        assert_frame_equal(
            log_collector.get_block_section_times_of_train(event_bus.run_id, "ice_4"),
            _enter_leave_block_section_4_df,
        )

    def test_departure_arrival_all(
        self, _departure_arrival_all_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(event_bus.run_id),
            _departure_arrival_all_df,
        )

    def test_departure_arrival_all_1(
        self, _departure_arrival_all_1_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_1(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(event_bus.run_id),
            _departure_arrival_all_1_df,
        )

    def test_departure_arrival_empty(
        self, event_bus: Logger, log_collector: LogCollector
    ):
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(event_bus.run_id),
            pd.DataFrame(
                columns=["train_id", "station_id", "arrival_tick", "departure_tick"]
            ),
        )

    def test_departure_arrival__multiple_runs(
        self,
        event_bus: Logger,
        event_bus2: Logger,
        log_collector: LogCollector,
        _departure_arrival_all_df,
    ):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        self.setup_departure_arrival_1(event_bus2)
        self.setup_departure_arrival_2(event_bus2)
        self.setup_departure_arrival_3(event_bus2)
        self.setup_departure_arrival_4(event_bus2)

        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(event_bus.run_id),
            _departure_arrival_all_df,
        )
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(event_bus2.run_id),
            _departure_arrival_all_df,
        )

    def test_enter_leave_block_section_all(
        self, _enter_leave_block_section_all_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_block_section_1(event_bus)
        self.setup_enter_leave_block_section_2(event_bus)
        self.setup_enter_leave_block_section_3(event_bus)
        self.setup_enter_leave_block_section_4(event_bus)
        assert_frame_equal(
            log_collector.get_block_section_times_all_trains(event_bus.run_id),
            _enter_leave_block_section_all_df,
        )

    def test_get_train_spawn_times(
        self,
        train_spawn_times_df: pd.DataFrame,
        event_bus: Logger,
        log_collector: LogCollector,
    ):
        self.setup_logs_spawn_trains(event_bus)
        assert_frame_equal(
            train_spawn_times_df, log_collector.get_train_spawn_times(event_bus.run_id)
        )

    def test_get_faults(
        self,
        faults_log_collector_df,
        event_bus,
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
            event_bus,
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
        generated_faults_df = log_collector.get_faults(event_bus.run_id)
        print(generated_faults_df)
        print(faults_log_collector_df)
        assert_frame_equal(generated_faults_df, faults_log_collector_df)
