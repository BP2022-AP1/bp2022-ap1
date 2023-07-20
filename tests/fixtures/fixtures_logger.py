import os
from datetime import datetime

import pandas as pd
import pytest

from src.data_science.data_science import DataScience
from src.data_science.grafana_data_registration import GrafanaDataRegistrator
from src.event_bus.event_bus import EventBus
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
from src.schedule.schedule_configuration import ScheduleConfiguration
from tests.logger.test_log_collector import TestLogCollector


@pytest.fixture
def event_bus(run):
    bus = EventBus(run_id=run.id)
    Logger(event_bus=bus)
    return bus


@pytest.fixture
def event_bus2(run2):
    bus = EventBus(run_id=run2.id)
    Logger(event_bus=bus)
    return bus


@pytest.fixture
def log_collector():
    return LogCollector()


@pytest.fixture
def data_science():
    return DataScience()


@pytest.fixture
def train_id():
    return "Test Train id"


@pytest.fixture
def station_id():
    return "Test Station id"


@pytest.fixture
def fahrstrasse():
    return "Test Fahrstrasse"


@pytest.fixture
def signal_id():
    return "Test-Signal"


@pytest.fixture
def state_before():
    return 0


@pytest.fixture
def state_after():
    return 1


@pytest.fixture
def edge_id():
    return "Test Block Section id"


@pytest.fixture
def edge_length():
    return 101.53


@pytest.fixture
def affected_element():
    return "Test Affected Element"


@pytest.fixture
def value_before():
    return "Test Value Before"


@pytest.fixture
def value_after():
    return "Test Value After"


@pytest.fixture
def trains():
    return ["cargo_4_cargo", "ice_1_passenger", "ice_2_passenger", "ice_3_passenger"]


@pytest.fixture
def stations():
    return ["station_1", "station_2", "station_3"]


@pytest.fixture
def run_ids(run: Run, run2: Run):
    return sorted([run.readable_id, run2.readable_id])


@pytest.fixture
def config_ids(simulation_configuration, simulation_configuration2):
    return sorted(
        [simulation_configuration.readable_id, simulation_configuration2.readable_id]
    )


@pytest.fixture
def platform_blocked_fault_configuration():
    return PlatformBlockedFaultConfiguration.create(
        start_time=10, end_time=20, affected_element_id="station_1", strategy="regular"
    )


@pytest.fixture
def track_blocked_fault_configuration():
    return TrackBlockedFaultConfiguration.create(
        start_time=10, end_time=20, affected_element_id="section_1", strategy="regular"
    )


@pytest.fixture
def track_speed_limit_fault_configuration():
    return TrackSpeedLimitFaultConfiguration.create(
        start_time=10,
        end_time=20,
        affected_element_id="section_1",
        new_speed_limit=10,
        strategy="regular",
    )


@pytest.fixture
def schedule_blocked_fault_configuration():
    return ScheduleBlockedFaultConfiguration.create(
        start_time=10,
        end_time=20,
        affected_element_id="ice_1_passenger",
        strategy="regular",
    )


@pytest.fixture
def train_prio_fault_configuration():
    return TrainPrioFaultConfiguration.create(
        start_time=10,
        end_time=20,
        affected_element_id="ice_1_passenger",
        new_prio=1,
        strategy="regular",
    )


@pytest.fixture
def train_speed_fault_configuration():
    return TrainSpeedFaultConfiguration.create(
        start_time=10,
        end_time=20,
        affected_element_id="ice_1_passenger",
        new_speed=10,
        strategy="regular",
    )


def second_to_tick(second: int) -> int:
    return int(float(second) / float(os.getenv("TICK_LENGTH")))


@pytest.fixture
def faults_log_collector_df(
    platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
    track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
    track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
    schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
    train_prio_fault_configuration: TrainPrioFaultConfiguration,
    train_speed_fault_configuration: TrainSpeedFaultConfiguration,
):
    faults_df = pd.DataFrame(
        {
            "begin_tick": [second_to_tick(10) for _ in range(6)],
            "fault_type": [
                "platform_blocked",
                "track_blocked",
                "track_speed_limit",
                "schedule_blocked",
                "train_prio",
                "train_speed",
            ],
            "fault_id": [
                platform_blocked_fault_configuration.id,
                track_blocked_fault_configuration.id,
                track_speed_limit_fault_configuration.id,
                schedule_blocked_fault_configuration.id,
                train_prio_fault_configuration.id,
                train_speed_fault_configuration.id,
            ],
            "affected_element": [
                "station_1",
                "section_1",
                "section_1",
                "ice_1_passenger",
                "ice_1_passenger",
                "ice_1_passenger",
            ],
            "value_before": [None, None, "100", None, "2", "100"],
            "value_after": [None, None, "10", None, "1", "10"],
            "end_tick": [second_to_tick(20) for _ in range(6)],
        }
    )
    return faults_df


@pytest.fixture
def faults_df(
    faults_log_collector_df: pd.DataFrame,
):
    faults_log_collector_df.insert(
        loc=0,
        column="begin_time",
        value=pd.Series([datetime(2020, 1, 1, 0, 0, 10, 0) for _ in range(6)]),
    )
    faults_log_collector_df.insert(
        loc=8,
        column="end_time",
        value=pd.Series([datetime(2020, 1, 1, 0, 0, 20, 0) for _ in range(6)]),
    )
    faults_log_collector_df.insert(
        loc=9,
        column="title",
        value=pd.Series(
            [
                "Platform blocked",
                "Track blocked",
                "Track speed limit",
                "Schedule blocked",
                "Train prio",
                "Train speed",
            ]
        ),
    )
    faults_log_collector_df.set_index("begin_time", inplace=True)
    return faults_log_collector_df


@pytest.fixture
def verkehrsleistung_time_df():
    verkehrsleistung_time_df = pd.DataFrame(
        {
            "time": [
                datetime(2020, 1, 1, 0, 1 if i == 6 else 0, (10 * i) % 60)
                for i in range(0, 7)
            ],
            "verkehrsleistung": [0.0, 0.0, 3780.0, 2520.0, 9270.0, 7416.0, 9840.0],
        }
    )
    verkehrsleistung_time_df.set_index("time", inplace=True)
    return verkehrsleistung_time_df


@pytest.fixture
def verkehrsleistung_momentarily_time_df():
    verkehrsleistung_time_df = pd.DataFrame(
        {
            "time": [
                datetime(2020, 1, 1, 0, 1 if i == 6 else 0, (10 * i) % 60)
                for i in range(0, 7)
            ],
            "verkehrsleistung": [0.0, 0.0, 7.560, 0.0, 29.520, 0.0, 21.960],
        }
    )
    verkehrsleistung_time_df.set_index("time", inplace=True)
    return verkehrsleistung_time_df


@pytest.fixture
def coal_demand_by_run_id_head_df(
    demand_train_schedule_configuration: ScheduleConfiguration,
):
    coal_demand_by_run_id_head_df = pd.DataFrame(
        {
            "time": [
                datetime(2020, 1, 1, int((16 + i * 15) / 60), (16 + i * 15) % 60, 40)
                for i in range(0, 10)
            ],
            f"value_{demand_train_schedule_configuration.id}": pd.Series(
                [
                    110.926498,
                    219.041547,
                    61.140221,
                    69.72047,
                    184.767735,
                    257.978718,
                    25.506843,
                    192.085535,
                    257.341683,
                    35.686849,
                ]
            ),
        }
    )
    coal_demand_by_run_id_head_df.set_index("time", inplace=True)
    return coal_demand_by_run_id_head_df


@pytest.fixture
def train_spawn_times_df():
    train_spawn_times_df = pd.DataFrame(
        {
            "tick": [
                second_to_tick(4600),
                second_to_tick(7300),
                second_to_tick(10900),
                second_to_tick(13600),
                second_to_tick(17200),
            ],
            f"train_id": [f"Kohlezug {i}" for i in range(1, 6)],
        }
    )
    return train_spawn_times_df


@pytest.fixture
def spawn_events_by_run_id_df():
    spawn_events_by_run_id_head_df = pd.DataFrame(
        {
            "time": [
                datetime(2020, 1, 1, 1, 16, 40),
                datetime(2020, 1, 1, 2, 1, 40),
                datetime(2020, 1, 1, 3, 1, 40),
                datetime(2020, 1, 1, 3, 46, 40),
                datetime(2020, 1, 1, 4, 46, 40),
            ],
            f"title": [f"Spawn train Kohlezug {i}" for i in range(1, 6)],
        }
    )
    spawn_events_by_run_id_head_df.set_index("time", inplace=True)
    return spawn_events_by_run_id_head_df


@pytest.fixture
def spawn_coal_events_by_config_id_head_df(
    demand_train_schedule_configuration: ScheduleConfiguration,
):
    spawn_events_by_run_id_head_df = pd.DataFrame(
        {
            "time": [
                datetime(2020, 1, 1, 1, 16, 40),
                datetime(2020, 1, 1, 2, 1, 40),
                datetime(2020, 1, 1, 3, 1, 40),
                datetime(2020, 1, 1, 3, 46, 40),
                datetime(2020, 1, 1, 4, 46, 40),
            ],
            f"title": [
                f"Spawn train from config {demand_train_schedule_configuration.id}"
                for _ in range(1, 6)
            ],
        }
    )
    spawn_events_by_run_id_head_df.set_index("time", inplace=True)
    return spawn_events_by_run_id_head_df


@pytest.fixture
def verkehrsarbeit_df():
    return pd.DataFrame(
        {
            "train_type": ["cargo", "passenger", "all"],
            "verkehrsarbeit": [0.0205, 0.1435, 0.164],
        }
    )


@pytest.fixture
def verkehrsleistung_by_run_id_df():
    return pd.DataFrame(
        {
            "train_type": ["cargo", "passenger", "all"],
            "enter_tick": pd.Series([0, 0, 0], dtype="Int64"),
            "leave_tick": pd.Series(
                [second_to_tick(40), second_to_tick(60), second_to_tick(60)],
                dtype="Int64",
            ),
            "edge_length": [20.5, 143.5, 164.0],
            "verkehrsleistung": [1.8450, 8.610000000000001, 9.84],
        }
    )


@pytest.fixture
def window_size_time_by_config_id_df():
    window_size_df = pd.DataFrame(
        {
            "time": [
                datetime(2020, 1, 1, 0, int((10 * i) / 60), (10 * i) % 60)
                for i in range(7)
            ],
            "arrival_size": pd.Series([0.0, 0.0, 5.0, 2.5, 7.5, 5.0, 25.0 / 3.0]),
            "departure_size": pd.Series(
                [0.0, 0.0, 0.0, 5.0, 5.0, 20.0 / 3.0, 20.0 / 3.0]
            ),
        }
    )
    window_size_df.set_index("time", inplace=True)
    return window_size_df


@pytest.fixture
def window_by_config_id_df():
    return pd.DataFrame(
        {
            "train_type": ["all", "cargo", "passenger"],
            "arrival_tick": [25 / 3, 20 / 3, 80 / 9],
            "departure_tick": [25 / 3, 20 / 3, 80 / 9],
        }
    )


@pytest.fixture
def window_all_by_config_id_df():
    return pd.DataFrame(
        {
            "station_id": [
                "station_1",
                "station_1",
                "station_1",
                "station_1",
                "station_2",
                "station_2",
                "station_2",
                "station_2",
                "station_3",
                "station_3",
                "station_3",
                "station_3",
            ],
            "train_id": [
                "cargo_4_cargo",
                "ice_1_passenger",
                "ice_2_passenger",
                "ice_3_passenger",
                "cargo_4_cargo",
                "ice_1_passenger",
                "ice_2_passenger",
                "ice_3_passenger",
                "cargo_4_cargo",
                "ice_1_passenger",
                "ice_2_passenger",
                "ice_3_passenger",
            ],
            "arrival_second": pd.Series(
                [0, 10, 10, 0, 10, 10, 10, 10, 10, 10, 10, 10], dtype="Int64"
            ),
            "departure_second": pd.Series(
                [10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 0, 10], dtype="Int64"
            ),
        }
    )


@pytest.fixture
def verkehrsarbeit_by_config_id_df(run):
    verkehrsarbeit_df = pd.DataFrame(
        {
            "run_id": [run.id],
            "edge_length": pd.Series([164.0]),
        }
    )
    verkehrsarbeit_df.set_index("run_id", inplace=True)
    return verkehrsarbeit_df


@pytest.fixture
def verkehrsleistung_by_config_id_df(run):
    verkehrsleistung_df = pd.DataFrame(
        {
            "run_id": [run.id],
            "edge_length": pd.Series([164.0]),
            "verkehrsleistung": pd.Series([9.840]),
        }
    )
    verkehrsleistung_df.set_index("run_id", inplace=True)
    return verkehrsleistung_df


@pytest.fixture
def average_verkehrsarbeit_by_config_id_df():
    verkehrsarbeit = pd.DataFrame(
        {
            "train_type": ["all", "cargo", "passenger"],
            "verkehrsarbeit": pd.Series([0.16399999999999998, 0.0205, 0.1435]),
        }
    )
    return verkehrsarbeit


@pytest.fixture
def average_verkehrsleistung_by_config_id_df():
    verkehrsleistung = pd.DataFrame(
        {
            "train_type": ["all", "cargo", "passenger"],
            "verkehrsleistung": pd.Series([9.840, 1.845, 8.610]),
        }
    )
    return verkehrsleistung


@pytest.fixture
def window_by_multi_config_df(simulation_configuration):
    return pd.DataFrame(
        {
            "config_readable_id": [
                simulation_configuration.readable_id,
                simulation_configuration.readable_id,
                simulation_configuration.readable_id,
            ],
            "train_type": ["all", "cargo", "passenger"],
            "arrival_second": pd.Series([25 / 3, 20 / 3, 80 / 9]),
            "departure_second": pd.Series([25 / 3, 20 / 3, 80 / 9]),
        }
    )


@pytest.fixture
def verkehrsarbeit_by_multi_config_df(simulation_configuration):
    return pd.DataFrame(
        {
            "config_readable_id": [
                simulation_configuration.readable_id,
                simulation_configuration.readable_id,
                simulation_configuration.readable_id,
            ],
            "train_type": ["all", "cargo", "passenger"],
            "edge_length": pd.Series([0.164, 0.0205, 0.1435]),
        }
    )


@pytest.fixture
def verkehrsleistung_by_multi_config_df(simulation_configuration):
    return pd.DataFrame(
        {
            "config_readable_id": [
                simulation_configuration.readable_id,
                simulation_configuration.readable_id,
                simulation_configuration.readable_id,
            ],
            "train_type": ["all", "cargo", "passenger"],
            "verkehrsleistung": pd.Series([9.840, 1.845, 8.610]),
        }
    )


@pytest.fixture
def grafana_data_registrator():
    return GrafanaDataRegistrator()


def setup_logs_departure_arrival(event_bus):
    TestLogCollector.setup_departure_arrival_1(event_bus)
    TestLogCollector.setup_departure_arrival_2(event_bus)
    TestLogCollector.setup_departure_arrival_3(event_bus)
    TestLogCollector.setup_departure_arrival_4(event_bus)


def setup_logs_departure_arrival_alt(event_bus2):
    TestLogCollector.setup_departure_arrival_1_alt(event_bus2)
    TestLogCollector.setup_departure_arrival_2_alt(event_bus2)
    TestLogCollector.setup_departure_arrival_3_alt(event_bus2)
    TestLogCollector.setup_departure_arrival_4_alt(event_bus2)


def setup_logs_edges(event_bus):
    TestLogCollector.setup_enter_leave_edge_1(event_bus)
    TestLogCollector.setup_enter_leave_edge_2(event_bus)
    TestLogCollector.setup_enter_leave_edge_3(event_bus)
    TestLogCollector.setup_enter_leave_edge_4(event_bus)
