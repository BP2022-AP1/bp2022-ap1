import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.data_science.data_science import DataScience
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
from src.implementor.models import Run, SimulationConfiguration
from src.logger.logger import Logger
from src.schedule.demand_schedule_strategy import DemandScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)
from tests.decorators import recreate_db_setup
from tests.fixtures.fixtures_logger import (
    setup_logs_block_sections,
    setup_logs_departure_arrival,
    setup_logs_departure_arrival_alt,
)
from tests.logger.test_log_collector import TestLogCollector


# pylint: disable=too-many-public-methods
class TestDataScience:
    """Tests for the DataScience class"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_get_all_stations(
        self, logger: Logger, data_science: DataScience, stations
    ):
        setup_logs_departure_arrival(logger)
        _stations = data_science.get_all_stations()
        _stations = sorted(stations)
        assert _stations == stations

    def test_get_all_trains(self, logger: Logger, data_science: DataScience, trains):
        setup_logs_departure_arrival(logger)
        _trains = data_science.get_all_trains()
        _trains = sorted(_trains)
        assert _trains == trains

    def test_get_all_run_ids(
        self, logger: Logger, data_science: DataScience, run_ids: list[Run]
    ):
        setup_logs_departure_arrival(logger)
        _run_ids = data_science.get_all_run_ids()
        _run_ids = sorted(_run_ids)
        assert _run_ids == run_ids

    def test_get_all_config_ids(
        self, logger: Logger, data_science: DataScience, config_ids
    ):
        setup_logs_departure_arrival(logger)
        _config_ids = data_science.get_all_config_ids()
        _config_ids = sorted(_config_ids)
        assert _config_ids == config_ids

    def test_get_faults_by_run_id(
        self,
        logger: Logger,
        data_science: DataScience,
        platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
        track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
        track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        train_prio_fault_configuration: TrainPrioFaultConfiguration,
        train_speed_fault_configuration: TrainSpeedFaultConfiguration,
        faults_df: pd.DataFrame,
    ):
        # pylint: disable=duplicate-code
        TestLogCollector.setup_faults(
            logger,
            platform_blocked_fault_configuration,
            track_blocked_fault_configuration,
            track_speed_limit_fault_configuration,
            schedule_blocked_fault_configuration,
            train_prio_fault_configuration,
            train_speed_fault_configuration,
        )

        _faults_df = data_science.get_faults_by_run_id(logger.run_id)
        faults_df["fault_id"] = faults_df["fault_id"].astype("string")
        assert_frame_equal(_faults_df, faults_df)

    def test_get_verkehrsleistung_time_by_run_id(
        self,
        logger: Logger,
        data_science: DataScience,
        verkehrsleistung_time_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsleistung_df = data_science.get_verkehrsleistung_time_by_run_id(
            logger.run_id, delta_tick=10
        )
        assert_frame_equal(verkehrsleistung_df, verkehrsleistung_time_df)

    def test_get_verkehrsleistung_momentarily_time_by_run_id(
        self,
        logger: Logger,
        data_science: DataScience,
        verkehrsleistung_momentarily_time_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsleistung_df = (
            data_science.get_verkehrsleistung_momentarily_time_by_run_id(
                logger.run_id, delta_tick=10
            )
        )
        assert_frame_equal(verkehrsleistung_df, verkehrsleistung_momentarily_time_df)

    def test_get_coal_demand_by_run_id(
        self,
        run: Run,
        data_science: DataScience,
        demand_strategy: DemandScheduleStrategy,
        demand_train_schedule_configuration: ScheduleConfiguration,
        spawner_configuration: SpawnerConfiguration,
        simulation_configuration: SimulationConfiguration,
        coal_demand_by_run_id_head_df: pd.DataFrame,
    ):
        SpawnerConfigurationXSimulationConfiguration.create(
            simulation_configuration=simulation_configuration,
            spawner_configuration=spawner_configuration,
        )
        SpawnerConfigurationXSchedule.create(
            spawner_configuration_id=spawner_configuration.id,
            schedule_configuration_id=demand_train_schedule_configuration.id,
        )
        coal_demand_df = data_science.get_coal_demand_by_run_id(run).head(10)
        assert_frame_equal(coal_demand_df, coal_demand_by_run_id_head_df)

    def test_get_spawn_events_by_run_id(self, run: Run, data_science: DataScience):
        with pytest.raises(NotImplementedError):
            data_science.get_spawn_events_by_run_id(run)

    def test_get_verkehrsmenge_by_run_id(
        self, logger: Logger, data_science: DataScience, verkehrsmenge_df: pd.DataFrame
    ):
        setup_logs_block_sections(logger)
        _verkehrsmenge_df = data_science.get_verkehrsmenge_by_run_id(logger.run_id)
        assert_frame_equal(_verkehrsmenge_df, verkehrsmenge_df)

    def test_get_verkehrsleistung_by_run_id(
        self,
        logger: Logger,
        data_science: DataScience,
        verkehrsleistung_by_run_id_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsleistung_df = data_science.get_verkehrsleistung_by_run_id(logger.run_id)
        assert_frame_equal(verkehrsleistung_df, verkehrsleistung_by_run_id_df)

    def test_get_station_counts_by_run_id(self, run: Run, data_science: DataScience):
        with pytest.raises(NotImplementedError):
            data_science.get_station_counts_by_run_id(run)

    def test_get_window_time_by_config_id(
        self,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
    ):
        with pytest.raises(NotImplementedError):
            data_science.get_window_time_by_config_id(simulation_configuration)

    def test_get_verkehrsleistung_time_by_config_id(
        self,
        simulation_configuration: SimulationConfiguration,
        logger: Logger,
        data_science: DataScience,
        verkehrsleistung_momentarily_time_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsleistung_df = data_science.get_verkehrsleistung_time_by_config_id(
            simulation_configuration, delta_tick=10
        )
        assert_frame_equal(verkehrsleistung_df, verkehrsleistung_momentarily_time_df)

    def test_get_coal_demand_by_config_id(
        self,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
    ):
        with pytest.raises(NotImplementedError):
            data_science.get_coal_demand_by_config_id(simulation_configuration)

    def test_get_spawn_events_by_config_id(
        self,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
    ):
        with pytest.raises(NotImplementedError):
            data_science.get_spawn_events_by_config_id(simulation_configuration)

    def test_get_window_by_config_id(
        self,
        simulation_configuration: SimulationConfiguration,
        logger: Logger,
        logger2: Logger,
        data_science: DataScience,
        window_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_departure_arrival(logger)
        setup_logs_departure_arrival_alt(logger2)
        window_df = data_science.get_window_by_config_id(
            simulation_configuration, threshold=0.7
        )
        assert_frame_equal(window_df, window_by_config_id_df)

    def test_get_window_all_by_config_id(
        self,
        simulation_configuration: SimulationConfiguration,
        logger: Logger,
        logger2: Logger,
        data_science: DataScience,
        window_all_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_departure_arrival(logger)
        setup_logs_departure_arrival_alt(logger2)
        window_df = data_science.get_window_all_by_config_id(simulation_configuration)
        assert_frame_equal(window_df, window_all_by_config_id_df)

    def test_get_verkehrsmenge_by_config_id(
        self,
        logger: Logger,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
        verkehrsmenge_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsmenge_df = data_science.get_verkehrsmenge_by_config_id(
            simulation_configuration
        )
        assert_frame_equal(verkehrsmenge_df, verkehrsmenge_by_config_id_df)

    def test_get_verkehrsleistung_by_config_id(
        self,
        logger: Logger,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
        verkehrsleistung_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsmenge_df = data_science.get_verkehrsleistung_by_config_id(
            simulation_configuration
        )
        assert_frame_equal(verkehrsmenge_df, verkehrsleistung_by_config_id_df)

    def test_get_window_by_multi_config(
        self,
        logger: Logger,
        logger2: Logger,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
        window_by_multi_config_df: pd.DataFrame,
    ):
        setup_logs_departure_arrival(logger)
        setup_logs_departure_arrival_alt(logger2)
        window_df = data_science.get_window_by_multi_config([simulation_configuration])
        assert_frame_equal(window_df, window_by_multi_config_df)

    def test_get_verkehrsmenge_by_multi_config(
        self,
        logger: Logger,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
        verkehrsmenge_by_multi_config_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsmenge_df = data_science.get_verkehrsmenge_by_multi_config(
            [simulation_configuration]
        )
        assert_frame_equal(verkehrsmenge_df, verkehrsmenge_by_multi_config_df)

    def test_get_verkehrsleistung_by_multi_config(
        self,
        logger: Logger,
        simulation_configuration: SimulationConfiguration,
        data_science: DataScience,
        verkehrsleistung_by_multi_config_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        verkehrsleistung_df = data_science.get_verkehrsleistung_by_multi_config(
            [simulation_configuration]
        )
        assert_frame_equal(verkehrsleistung_df, verkehrsleistung_by_multi_config_df)
