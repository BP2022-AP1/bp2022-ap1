import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

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
from src.logger.logger import Logger
from tests.decorators import recreate_db_setup
from tests.fixtures.fixtures_logger import (
    setup_logs_block_sections,
    setup_logs_departure_arrival,
    setup_logs_departure_arrival_alt,
)
from tests.logger.test_log_collector import TestLogCollector


# pylint: disable=too-many-public-methods
class TestGrafanaDataRegistration:
    """Tests for the GrafanaDataRegistration class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def _run_id(self, run):
        return str(run.id)

    @pytest.fixture
    def _config_id(self, simulation_configuration):
        return str(simulation_configuration.id)

    @pytest.fixture
    def _multi_config(self, simulation_configuration):
        return str(simulation_configuration)

    @pytest.fixture
    def _search_list(self):
        return [
            "get_faults_by_run_id:${run_id}",
            "get_verkehrsleistung_time_by_run_id:${run_id}",
            "get_verkehrsleistung_momentarily_time_by_run_id:${run_id}",
            "get_verkehrsmenge_by_run_id:${run_id}",
            "get_verkehrsleistung_by_run_id:${run_id}",
            "get_verkehrsleistung_time_by_config_id:${config_id}",
            "get_window_by_config_id:${config_id}",
            "get_window_all_by_config_id:${config_id}",
            "get_verkehrsmenge_by_config_id:${config_id}",
            "get_verkehrsleistung_by_config_id:${config_id}",
            "get_window_by_multi_config:${config_ids}",
            "get_verkehrsmenge_by_multi_config:${config_ids}",
            "get_verkehrsleistung_by_multi_config:${config_ids}",
        ]

    def test_get_faults_by_run_id(
        self,
        _run_id: str,
        logger: Logger,
        platform_blocked_fault_configuration: PlatformBlockedFaultConfiguration,
        track_blocked_fault_configuration: TrackBlockedFaultConfiguration,
        track_speed_limit_fault_configuration: TrackSpeedLimitFaultConfiguration,
        schedule_blocked_fault_configuration: ScheduleBlockedFaultConfiguration,
        train_prio_fault_configuration: TrainPrioFaultConfiguration,
        train_speed_fault_configuration: TrainSpeedFaultConfiguration,
        faults_df: pd.DataFrame,
        grafana_data_registrator: GrafanaDataRegistrator,
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
        _faults_df = grafana_data_registrator.get_faults_by_run_id(_run_id, None)
        faults_df["fault_id"] = faults_df["fault_id"].astype("string")
        assert_frame_equal(_faults_df, faults_df)

    def test_get_verkehrsleistung_time_by_run_id(
        self,
        _run_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsleistung_time_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsleistung_time_by_run_id(_run_id, None),
            verkehrsleistung_time_df,
        )

    def test_get_verkehrsleistung_momentarily_time_by_run_id(
        self,
        _run_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsleistung_momentarily_time_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsleistung_momentarily_time_by_run_id(
                _run_id, None
            ),
            verkehrsleistung_momentarily_time_df,
        )

    def test_get_verkehrsmenge_by_run_id(
        self,
        _run_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsmenge_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsmenge_by_run_id(_run_id, None),
            verkehrsmenge_df,
        )

    def test_get_verkehrsleistung_by_run_id(
        self,
        _run_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsleistung_by_run_id_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsleistung_by_run_id(_run_id, None),
            verkehrsleistung_by_run_id_df,
        )

    # --- CONFIG

    def test_get_verkehrsleistung_time_by_config_id(
        self,
        _config_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsleistung_momentarily_time_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsleistung_time_by_config_id(
                _config_id, None
            ),
            verkehrsleistung_momentarily_time_df,
        )

    def test_get_window_by_config_id(
        self,
        _config_id: str,
        logger: Logger,
        logger2: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        window_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_departure_arrival(logger)
        setup_logs_departure_arrival_alt(logger2)
        assert_frame_equal(
            grafana_data_registrator.get_window_by_config_id(_config_id, None),
            window_by_config_id_df,
        )

    def test_get_window_all_by_config_id(
        self,
        _config_id: str,
        logger: Logger,
        logger2: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        window_all_by_config_id_df,
    ):
        setup_logs_departure_arrival(logger)
        setup_logs_departure_arrival_alt(logger2)
        assert_frame_equal(
            grafana_data_registrator.get_window_all_by_config_id(_config_id, None),
            window_all_by_config_id_df,
        )

    def test_get_verkehrsmenge_by_config_id(
        self,
        _config_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsmenge_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsmenge_by_config_id(_config_id, None),
            verkehrsmenge_by_config_id_df,
        )

    def test_get_verkehrsleistung_by_config_id(
        self,
        _config_id: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsleistung_by_config_id_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsleistung_by_config_id(
                _config_id, None
            ),
            verkehrsleistung_by_config_id_df,
        )

    # --- MULTI CONFIG

    def test_get_window_by_multi_config(
        self,
        _multi_config: str,
        logger: Logger,
        logger2: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        window_by_multi_config_df: pd.DataFrame,
    ):
        setup_logs_departure_arrival(logger)
        setup_logs_departure_arrival_alt(logger2)
        assert_frame_equal(
            grafana_data_registrator.get_window_by_multi_config(_multi_config, None),
            window_by_multi_config_df,
        )

    def test_get_verkehrsmenge_by_multi_config(
        self,
        _multi_config: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsmenge_by_multi_config_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsmenge_by_multi_config(
                _multi_config, None
            ),
            verkehrsmenge_by_multi_config_df,
        )

    def test_get_verkehrsleistung_by_multi_config(
        self,
        _multi_config: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        verkehrsleistung_by_multi_config_df: pd.DataFrame,
    ):
        setup_logs_block_sections(logger)
        assert_frame_equal(
            grafana_data_registrator.get_verkehrsleistung_by_multi_config(
                _multi_config, None
            ),
            verkehrsleistung_by_multi_config_df,
        )

    # -- FINDERS

    def test_get_all_station_ids(
        self,
        _multi_config: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        stations,
    ):
        setup_logs_departure_arrival(logger)
        assert sorted(grafana_data_registrator.get_all_station_ids(None)) == stations

    def test_get_all_train_ids(
        self,
        _multi_config: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        trains,
    ):
        setup_logs_block_sections(logger)
        assert sorted(grafana_data_registrator.get_all_train_ids(None)) == trains

    def test_get_all_run_ids(
        self,
        _multi_config: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        run_ids,
    ):
        setup_logs_block_sections(logger)
        assert grafana_data_registrator.get_all_run_ids(None) == run_ids

    def test_get_all_config_ids(
        self,
        _multi_config: str,
        logger: Logger,
        grafana_data_registrator: GrafanaDataRegistrator,
        config_ids,
    ):
        setup_logs_block_sections(logger)
        assert grafana_data_registrator.get_all_config_ids(None) == config_ids

    def test_search(
        self, grafana_data_registrator: GrafanaDataRegistrator, _search_list
    ):
        assert grafana_data_registrator.search(None) == _search_list