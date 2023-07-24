import os

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.event_bus.event_bus import EventBus
from src.implementor.models import Run
from src.logger.log_collector import LogCollector
from tests.decorators import recreate_db_setup


# pylint: disable=too-many-public-methods
class TestLogCollector:
    """Tests for the LogCollector class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @staticmethod
    def second_to_tick(second: int) -> int:
        return int(float(second) / float(os.getenv("TICK_LENGTH")))

    @pytest.fixture
    def _run_ids(self, run: Run):
        return [run.readable_id]

    @pytest.fixture
    def _config_ids(self, simulation_configuration):
        return [simulation_configuration.readable_id]

    @pytest.fixture
    def _departure_arrival_1_df(self):
        departure_arrival_df = pd.DataFrame(
            [
                ["station_1", self.second_to_tick(10), self.second_to_tick(20)],
                ["station_2", self.second_to_tick(30), self.second_to_tick(40)],
                ["station_3", self.second_to_tick(50), self.second_to_tick(60)],
            ],
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
                [
                    "station_1",
                    self.second_to_tick(10),
                    self.second_to_tick(20),
                    "ice_1_passenger",
                ],
                [
                    "station_2",
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "ice_1_passenger",
                ],
                [
                    "station_3",
                    self.second_to_tick(50),
                    self.second_to_tick(60),
                    "ice_1_passenger",
                ],
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
            [
                ["station_1", self.second_to_tick(10), self.second_to_tick(20)],
                ["station_2", self.second_to_tick(30), self.second_to_tick(40)],
                ["station_3", self.second_to_tick(50), None],
            ],
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
            [
                ["station_1", None, self.second_to_tick(20)],
                ["station_2", self.second_to_tick(30), self.second_to_tick(40)],
                ["station_3", self.second_to_tick(50), self.second_to_tick(60)],
            ],
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
            [
                ["station_1", None, self.second_to_tick(20)],
                ["station_2", self.second_to_tick(30), self.second_to_tick(40)],
                ["station_3", self.second_to_tick(50), None],
            ],
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
                ["station_1", None, self.second_to_tick(20), "cargo_4_cargo"],
                [
                    "station_2",
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "cargo_4_cargo",
                ],
                ["station_3", self.second_to_tick(50), None, "cargo_4_cargo"],
                [
                    "station_1",
                    self.second_to_tick(10),
                    self.second_to_tick(20),
                    "ice_1_passenger",
                ],
                [
                    "station_2",
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "ice_1_passenger",
                ],
                [
                    "station_3",
                    self.second_to_tick(50),
                    self.second_to_tick(60),
                    "ice_1_passenger",
                ],
                [
                    "station_1",
                    self.second_to_tick(10),
                    self.second_to_tick(20),
                    "ice_2_passenger",
                ],
                [
                    "station_2",
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "ice_2_passenger",
                ],
                ["station_3", self.second_to_tick(50), None, "ice_2_passenger"],
                ["station_1", None, self.second_to_tick(20), "ice_3_passenger"],
                [
                    "station_2",
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "ice_3_passenger",
                ],
                [
                    "station_3",
                    self.second_to_tick(50),
                    self.second_to_tick(60),
                    "ice_3_passenger",
                ],
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
    def _enter_leave_edge_1_df(self):
        return pd.DataFrame(
            [
                [self.second_to_tick(10), self.second_to_tick(20), "section_1", 10.5],
                [self.second_to_tick(30), self.second_to_tick(40), "section_2", 20.5],
                [self.second_to_tick(50), self.second_to_tick(60), "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "edge_id",
                "edge_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_edge_2_df(self):
        return pd.DataFrame(
            [
                [self.second_to_tick(10), self.second_to_tick(20), "section_1", 10.5],
                [self.second_to_tick(30), self.second_to_tick(40), "section_2", 20.5],
                [self.second_to_tick(50), None, "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "edge_id",
                "edge_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_edge_3_df(self):
        return pd.DataFrame(
            [
                [None, self.second_to_tick(20), "section_1", None],
                [self.second_to_tick(30), self.second_to_tick(40), "section_2", 20.5],
                [self.second_to_tick(50), self.second_to_tick(60), "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "edge_id",
                "edge_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_edge_4_df(self):
        return pd.DataFrame(
            [
                [None, self.second_to_tick(20), "section_1", None],
                [self.second_to_tick(30), self.second_to_tick(40), "section_2", 20.5],
                [self.second_to_tick(50), None, "section_3", 30.5],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "edge_id",
                "edge_length",
            ],
        )

    @pytest.fixture
    def _enter_leave_edge_all_df(self):
        return pd.DataFrame(
            [
                [None, self.second_to_tick(20), "section_1", None, "cargo_4_cargo"],
                [
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "section_2",
                    20.5,
                    "cargo_4_cargo",
                ],
                [self.second_to_tick(50), None, "section_3", 30.5, "cargo_4_cargo"],
                [
                    self.second_to_tick(10),
                    self.second_to_tick(20),
                    "section_1",
                    10.5,
                    "ice_1_passenger",
                ],
                [
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "section_2",
                    20.5,
                    "ice_1_passenger",
                ],
                [
                    self.second_to_tick(50),
                    self.second_to_tick(60),
                    "section_3",
                    30.5,
                    "ice_1_passenger",
                ],
                [
                    self.second_to_tick(10),
                    self.second_to_tick(20),
                    "section_1",
                    10.5,
                    "ice_2_passenger",
                ],
                [
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "section_2",
                    20.5,
                    "ice_2_passenger",
                ],
                [self.second_to_tick(50), None, "section_3", 30.5, "ice_2_passenger"],
                [None, self.second_to_tick(20), "section_1", None, "ice_3_passenger"],
                [
                    self.second_to_tick(30),
                    self.second_to_tick(40),
                    "section_2",
                    20.5,
                    "ice_3_passenger",
                ],
                [
                    self.second_to_tick(50),
                    self.second_to_tick(60),
                    "section_3",
                    30.5,
                    "ice_3_passenger",
                ],
            ],
            columns=[
                "enter_tick",
                "leave_tick",
                "edge_id",
                "edge_length",
                "train_id",
            ],
        )

    @staticmethod
    def setup_departure_arrival_1(event_bus):
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(10), "ice_1_passenger", "station_1"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(20), "ice_1_passenger", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(30), "ice_1_passenger", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(40), "ice_1_passenger", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(50), "ice_1_passenger", "station_3"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(60), "ice_1_passenger", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_2(event_bus):
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(10), "ice_2_passenger", "station_1"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(20), "ice_2_passenger", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(30), "ice_2_passenger", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(40), "ice_2_passenger", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(50), "ice_2_passenger", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_3(event_bus):
        event_bus.departure_train(
            TestLogCollector.second_to_tick(20), "ice_3_passenger", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(30), "ice_3_passenger", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(40), "ice_3_passenger", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(50), "ice_3_passenger", "station_3"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(60), "ice_3_passenger", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_4(event_bus):
        event_bus.departure_train(
            TestLogCollector.second_to_tick(20), "cargo_4_cargo", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(30), "cargo_4_cargo", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(40), "cargo_4_cargo", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(50), "cargo_4_cargo", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_1_alt(event_bus):
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(20), "ice_1_passenger", "station_1"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(30), "ice_1_passenger", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(40), "ice_1_passenger", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(50), "ice_1_passenger", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(60), "ice_1_passenger", "station_3"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(70), "ice_1_passenger", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_2_alt(event_bus):
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(20), "ice_2_passenger", "station_1"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(30), "ice_2_passenger", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(40), "ice_2_passenger", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(50), "ice_2_passenger", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(60), "ice_2_passenger", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_3_alt(event_bus):
        event_bus.departure_train(
            TestLogCollector.second_to_tick(30), "ice_3_passenger", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(40), "ice_3_passenger", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(50), "ice_3_passenger", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(60), "ice_3_passenger", "station_3"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(70), "ice_3_passenger", "station_3"
        )

    @staticmethod
    def setup_departure_arrival_4_alt(event_bus):
        event_bus.departure_train(
            TestLogCollector.second_to_tick(30), "cargo_4_cargo", "station_1"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(40), "cargo_4_cargo", "station_2"
        )
        event_bus.departure_train(
            TestLogCollector.second_to_tick(50), "cargo_4_cargo", "station_2"
        )
        event_bus.arrival_train(
            TestLogCollector.second_to_tick(60), "cargo_4_cargo", "station_3"
        )

    @staticmethod
    def setup_enter_leave_edge_1(event_bus):
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(10),
            "ice_1_passenger",
            "section_1",
            10.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(20),
            "ice_1_passenger",
            "section_1",
            10.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(30),
            "ice_1_passenger",
            "section_2",
            20.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(40),
            "ice_1_passenger",
            "section_2",
            20.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(50),
            "ice_1_passenger",
            "section_3",
            30.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(60),
            "ice_1_passenger",
            "section_3",
            30.5,
        )

    @staticmethod
    def setup_enter_leave_edge_2(event_bus):
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(10),
            "ice_2_passenger",
            "section_1",
            10.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(20),
            "ice_2_passenger",
            "section_1",
            10.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(30),
            "ice_2_passenger",
            "section_2",
            20.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(40),
            "ice_2_passenger",
            "section_2",
            20.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(50),
            "ice_2_passenger",
            "section_3",
            30.5,
        )

    @staticmethod
    def setup_enter_leave_edge_3(event_bus):
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(20),
            "ice_3_passenger",
            "section_1",
            10.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(30),
            "ice_3_passenger",
            "section_2",
            20.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(40),
            "ice_3_passenger",
            "section_2",
            20.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(50),
            "ice_3_passenger",
            "section_3",
            30.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(60),
            "ice_3_passenger",
            "section_3",
            30.5,
        )

    @staticmethod
    def setup_enter_leave_edge_4(event_bus):
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(20),
            "cargo_4_cargo",
            "section_1",
            10.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(30),
            "cargo_4_cargo",
            "section_2",
            20.5,
        )
        event_bus.train_leave_edge(
            TestLogCollector.second_to_tick(40),
            "cargo_4_cargo",
            "section_2",
            20.5,
        )
        event_bus.train_enter_edge(
            TestLogCollector.second_to_tick(50),
            "cargo_4_cargo",
            "section_3",
            30.5,
        )

    @staticmethod
    def setup_logs_spawn_trains(event_bus):
        event_bus.spawn_train(TestLogCollector.second_to_tick(4600), "Kohlezug 1")
        event_bus.spawn_train(TestLogCollector.second_to_tick(7300), "Kohlezug 2")
        event_bus.spawn_train(TestLogCollector.second_to_tick(10900), "Kohlezug 3")
        event_bus.spawn_train(TestLogCollector.second_to_tick(13600), "Kohlezug 4")
        event_bus.spawn_train(TestLogCollector.second_to_tick(17200), "Kohlezug 5")

    @staticmethod
    def setup_faults(
        event_bus: EventBus,
        platform_blocked_fault_configuration,
        track_blocked_fault_configuration,
        track_speed_limit_fault_configuration,
        schedule_blocked_fault_configuration,
        train_prio_fault_configuration,
        train_speed_fault_configuration,
    ):
        event_bus.inject_platform_blocked_fault(
            TestLogCollector.second_to_tick(10),
            platform_blocked_fault_configuration,
            "station_1",
        )
        event_bus.resolve_platform_blocked_fault(
            TestLogCollector.second_to_tick(20),
            platform_blocked_fault_configuration,
        )

        event_bus.inject_track_blocked_fault(
            TestLogCollector.second_to_tick(10),
            track_blocked_fault_configuration,
            "section_1",
        )
        event_bus.resolve_track_blocked_fault(
            TestLogCollector.second_to_tick(20), track_blocked_fault_configuration
        )

        event_bus.inject_track_speed_limit_fault(
            TestLogCollector.second_to_tick(10),
            track_speed_limit_fault_configuration,
            "section_1",
            "100",
            "10",
        )
        event_bus.resolve_track_speed_limit_fault(
            TestLogCollector.second_to_tick(20),
            track_speed_limit_fault_configuration,
        )

        event_bus.inject_schedule_blocked_fault(
            TestLogCollector.second_to_tick(10),
            schedule_blocked_fault_configuration,
            "ice_1_passenger",
        )
        event_bus.resolve_schedule_blocked_fault(
            TestLogCollector.second_to_tick(20),
            schedule_blocked_fault_configuration,
        )

        event_bus.inject_train_prio_fault(
            TestLogCollector.second_to_tick(10),
            train_prio_fault_configuration,
            "ice_1_passenger",
            "2",
            "1",
        )
        event_bus.resolve_train_prio_fault(
            TestLogCollector.second_to_tick(20), train_prio_fault_configuration
        )

        event_bus.inject_train_speed_fault(
            TestLogCollector.second_to_tick(10),
            train_speed_fault_configuration,
            "ice_1_passenger",
            "100",
            "10",
        )
        event_bus.resolve_train_speed_fault(
            TestLogCollector.second_to_tick(20), train_speed_fault_configuration
        )

    def test_get_trains(self, trains, event_bus, log_collector: LogCollector):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        _trains = log_collector.get_trains()
        _trains = sorted(_trains)
        assert _trains == trains

    def test_get_stations(self, stations, event_bus, log_collector: LogCollector):
        self.setup_departure_arrival_1(event_bus)
        self.setup_departure_arrival_2(event_bus)
        self.setup_departure_arrival_3(event_bus)
        self.setup_departure_arrival_4(event_bus)
        _stations = log_collector.get_stations()
        _stations = sorted(_stations)
        assert _stations == stations

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
            log_collector.get_departures_arrivals_of_train(
                event_bus.run_id, "ice_1_passenger"
            ),
            _departure_arrival_1_df,
        )

    def test_departure_arrival_2(
        self, _departure_arrival_2_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_2(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                event_bus.run_id, "ice_2_passenger"
            ),
            _departure_arrival_2_df,
        )

    def test_departure_arrival_3(
        self, _departure_arrival_3_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_3(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                event_bus.run_id, "ice_3_passenger"
            ),
            _departure_arrival_3_df,
        )

    def test_departure_arrival_4(
        self, _departure_arrival_4_df, event_bus, log_collector: LogCollector
    ):
        self.setup_departure_arrival_4(event_bus)
        assert_frame_equal(
            log_collector.get_departures_arrivals_of_train(
                event_bus.run_id, "cargo_4_cargo"
            ),
            _departure_arrival_4_df,
        )

    def test_enter_leave_edge_1(
        self, _enter_leave_edge_1_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_edge_1(event_bus)
        assert_frame_equal(
            log_collector.get_edge_times_of_train(event_bus.run_id, "ice_1_passenger"),
            _enter_leave_edge_1_df,
        )

    def test_enter_leave_edge_2(
        self, _enter_leave_edge_2_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_edge_2(event_bus)
        assert_frame_equal(
            log_collector.get_edge_times_of_train(event_bus.run_id, "ice_2_passenger"),
            _enter_leave_edge_2_df,
        )

    def test_enter_leave_edge_3(
        self, _enter_leave_edge_3_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_edge_3(event_bus)
        assert_frame_equal(
            log_collector.get_edge_times_of_train(event_bus.run_id, "ice_3_passenger"),
            _enter_leave_edge_3_df,
        )

    def test_enter_leave_edge_4(
        self, _enter_leave_edge_4_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_edge_4(event_bus)
        assert_frame_equal(
            log_collector.get_edge_times_of_train(event_bus.run_id, "cargo_4_cargo"),
            _enter_leave_edge_4_df,
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
        self, event_bus: EventBus, log_collector: LogCollector
    ):
        assert_frame_equal(
            log_collector.get_departures_arrivals_all_trains(event_bus.run_id),
            pd.DataFrame(
                columns=["train_id", "station_id", "arrival_tick", "departure_tick"]
            ),
        )

    def test_departure_arrival_multiple_runs(
        self,
        event_bus: EventBus,
        event_bus2: EventBus,
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

    def test_enter_leave_edge_all(
        self, _enter_leave_edge_all_df, event_bus, log_collector: LogCollector
    ):
        self.setup_enter_leave_edge_1(event_bus)
        self.setup_enter_leave_edge_2(event_bus)
        self.setup_enter_leave_edge_3(event_bus)
        self.setup_enter_leave_edge_4(event_bus)
        assert_frame_equal(
            log_collector.get_edge_times_all_trains(event_bus.run_id),
            _enter_leave_edge_all_df,
        )

    def test_get_train_spawn_times(
        self,
        train_spawn_times_df: pd.DataFrame,
        event_bus: EventBus,
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
        assert_frame_equal(generated_faults_df, faults_log_collector_df)
