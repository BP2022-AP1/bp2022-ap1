from datetime import datetime
from uuid import uuid4

import pandas as pd
import pytest

from src.data_science.data_science import DataScience
from src.data_science.grafana_data_registration import GrafanaDataRegistrator
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
from tests.logger.test_log_collector import TestLogCollector


@pytest.fixture
def logger(run):
    return Logger(run_id=run.id)


@pytest.fixture
def logger2(run2):
    return Logger(run_id=run2.id)


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
    return uuid4()


@pytest.fixture
def state_before():
    return 0


@pytest.fixture
def state_after():
    return 1


@pytest.fixture
def block_section_id():
    return "Test Block Section id"


@pytest.fixture
def block_section_length():
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
    return ["ice_1", "ice_2", "ice_3", "ice_4"]


@pytest.fixture
def stations():
    return ["station_1", "station_2", "station_3"]


@pytest.fixture
def run_ids(run: Run):
    return [run.id]


@pytest.fixture
def config_ids(simulation_configuration):
    return [simulation_configuration.id]


@pytest.fixture
def platform_blocked_fault_configuration():
    return PlatformBlockedFaultConfiguration.create(
        start_tick=10, end_tick=20, affected_element_id="station_1", strategy="regular"
    )


@pytest.fixture
def track_blocked_fault_configuration():
    return TrackBlockedFaultConfiguration.create(
        start_tick=10, end_tick=20, affected_element_id="section_1", strategy="regular"
    )


@pytest.fixture
def track_speed_limit_fault_configuration():
    return TrackSpeedLimitFaultConfiguration.create(
        start_tick=10,
        end_tick=20,
        affected_element_id="section_1",
        new_speed_limit=10,
        strategy="regular",
    )


@pytest.fixture
def schedule_blocked_fault_configuration():
    return ScheduleBlockedFaultConfiguration.create(
        start_tick=10, end_tick=20, affected_element_id="ice_1", strategy="regular"
    )


@pytest.fixture
def train_prio_fault_configuration():
    return TrainPrioFaultConfiguration.create(
        start_tick=10,
        end_tick=20,
        affected_element_id="ice_1",
        new_prio=1,
        strategy="regular",
    )


@pytest.fixture
def train_speed_fault_configuration():
    return TrainSpeedFaultConfiguration.create(
        start_tick=10,
        end_tick=20,
        affected_element_id="ice_1",
        new_speed=10,
        strategy="regular",
    )


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
            "begin_tick": [10, 10, 10, 10, 10, 10],
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
                "ice_1",
                "ice_1",
                "ice_1",
            ],
            "value_before": [None, None, "100", None, "2", "100"],
            "value_after": [None, None, "10", None, "1", "10"],
            "end_tick": [20, 20, 20, 20, 20, 20],
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
                for i in range(1, 7)
            ],
            "verkehrsleistung": [0.0, 7560.0, 3780.0, 12360.0, 9270.0, 11808.0],
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
                for i in range(1, 7)
            ],
            "verkehrsleistung": [0.0, 7560.0, 0.0, 29520.0, 0.0, 21960.0],
        }
    )
    verkehrsleistung_time_df.set_index("time", inplace=True)
    return verkehrsleistung_time_df


@pytest.fixture
def verkehrsmenge_df():
    return pd.DataFrame({"verkehrsmenge": [164.0]})


@pytest.fixture
def verkehrsleistung_by_run_id_df():
    return pd.DataFrame(
        {
            "enter_tick": [10.0],
            "leave_tick": [60.0],
            "block_section_length": [164.0],
            "verkehrsleistung": [11808.0],
        }
    )


@pytest.fixture
def window_by_config_id_df():
    return pd.DataFrame(
        {
            "arrival_tick": [25 / 3],
            "departure_tick": [25 / 3],
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
                "ice_1",
                "ice_2",
                "ice_3",
                "ice_4",
                "ice_1",
                "ice_2",
                "ice_3",
                "ice_4",
                "ice_1",
                "ice_2",
                "ice_3",
                "ice_4",
            ],
            "arrival_tick": pd.Series(
                [10, 10, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10], dtype="Int64"
            ),
            "departure_tick": pd.Series(
                [10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 10, 0], dtype="Int64"
            ),
        }
    )


@pytest.fixture
def verkehrsmenge_by_config_id_df(run):
    verkehrsmenge_df = pd.DataFrame(
        {
            "run_id": [run.id],
            "enter_tick": pd.Series([10], dtype="Int64"),
            "leave_tick": pd.Series([60], dtype="Int64"),
            "block_section_length": pd.Series([164.0]),
        }
    )
    verkehrsmenge_df.set_index("run_id", inplace=True)
    return verkehrsmenge_df


@pytest.fixture
def verkehrsleistung_by_config_id_df(run):
    verkehrsleistung_df = pd.DataFrame(
        {
            "run_id": [run.id],
            "enter_tick": pd.Series([10], dtype="Int64"),
            "leave_tick": pd.Series([60], dtype="Int64"),
            "block_section_length": pd.Series([164.0]),
            "verkehrsleistung": pd.Series([11808.0]),
        }
    )
    verkehrsleistung_df.set_index("run_id", inplace=True)
    return verkehrsleistung_df


@pytest.fixture
def window_by_multi_config_df(simulation_configuration):
    return pd.DataFrame(
        {
            "config_id": [simulation_configuration.id],
            "arrival_tick": pd.Series([25 / 3], dtype="Float64"),
            "departure_tick": pd.Series([25 / 3], dtype="Float64"),
        }
    )


@pytest.fixture
def verkehrsmenge_by_multi_config_df(simulation_configuration):
    return pd.DataFrame(
        {
            "config_id": [simulation_configuration.id],
            "block_section_length": pd.Series([164.0]),
        }
    )


@pytest.fixture
def verkehrsleistung_by_multi_config_df(simulation_configuration):
    return pd.DataFrame(
        {
            "config_id": [simulation_configuration.id],
            "enter_tick": pd.Series([10.0]),
            "leave_tick": pd.Series([60.0]),
            "block_section_length": pd.Series([164.0]),
            "verkehrsleistung": pd.Series([11808.0]),
        }
    )


@pytest.fixture
def grafana_data_registrator():
    return GrafanaDataRegistrator()


def setup_logs_departure_arrival(logger):
    TestLogCollector.setup_departure_arrival_1(logger)
    TestLogCollector.setup_departure_arrival_2(logger)
    TestLogCollector.setup_departure_arrival_3(logger)
    TestLogCollector.setup_departure_arrival_4(logger)


def setup_logs_departure_arrival_alt(logger2):
    TestLogCollector.setup_departure_arrival_1_alt(logger2)
    TestLogCollector.setup_departure_arrival_2_alt(logger2)
    TestLogCollector.setup_departure_arrival_3_alt(logger2)
    TestLogCollector.setup_departure_arrival_4_alt(logger2)


def setup_logs_block_sections(logger):
    TestLogCollector.setup_enter_leave_block_section_1(logger)
    TestLogCollector.setup_enter_leave_block_section_2(logger)
    TestLogCollector.setup_enter_leave_block_section_3(logger)
    TestLogCollector.setup_enter_leave_block_section_4(logger)
