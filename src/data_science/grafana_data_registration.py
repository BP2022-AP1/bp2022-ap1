from uuid import UUID

import pandas as pd
from grafana_pandas_datasource.registry import data_generators as dg

from src.data_science.data_science import DataScience


class GrafanaDataRegistrator:
    """Class that encapsulates all functions that are used by grafana"""

    def __init__(self):
        """Constructor of GrafanaDataRegistrator"""
        self.data_science = DataScience()

    # -- METRICS

    # --- RUN

    def get_faults_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns a list of all faults by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of faults
        """
        run_id = UUID(param)
        return self.data_science.get_faults_by_run_id(run_id)

    def get_verkehrsleistung_time_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns a list of all faults by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung"""
        run_id = UUID(param)
        return self.data_science.get_verkehrsleistung_time_by_run_id(run_id)

    def get_verkehrsleistung_momentarily_time_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the momentary verkehrsleistung over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung over time"""
        run_id = UUID(param)
        return self.data_science.get_verkehrsleistung_momentarily_time_by_run_id(run_id)

    def get_coal_demand_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the coal demand over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of coal demand over time"""
        run_id = UUID(param)
        return self.data_science.get_coal_demand_by_run_id(run_id)

    def get_spawn_events_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the train spawn events over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of all train spawn events over time
        """
        run_id = UUID(param)
        return self.data_science.get_spawn_events_by_run_id(run_id)

    def get_verkehrsmenge_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsmenge by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsmenge"""
        run_id = UUID(param)
        return self.data_science.get_verkehrsmenge_by_run_id(run_id)

    def get_verkehrsleistung_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung"""
        run_id = UUID(param)
        return self.data_science.get_verkehrsleistung_by_run_id(run_id)

    # --- CONFIG

    def get_verkehrsleistung_time_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung over time"""
        config_id = UUID(param)
        return self.data_science.get_verkehrsleistung_time_by_config_id(config_id)

    def get_window_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the window size of the entire network by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of window size"""
        config_id = UUID(param)
        return self.data_science.get_window_by_config_id(config_id)

    def get_window_all_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns window sizes of stations and trains by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of window sizes of stations and trains"""
        config_id = UUID(param)
        return self.data_science.get_window_all_by_config_id(config_id)

    def get_verkehrsmenge_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsmenge by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsmenge"""
        config_id = UUID(param)
        return self.data_science.get_verkehrsmenge_by_config_id(config_id)

    def get_verkehrsleistung_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung"""
        config_id = UUID(param)
        return self.data_science.get_verkehrsleistung_by_config_id(config_id)

    # --- MULTI CONFIG

    def get_window_by_multi_config(self, param, _) -> pd.DataFrame:
        """Returns multiple windows by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of multiple windows"""
        config_ids = [
            UUID(x) for x in param.replace(")", "").replace("(", "").split("|")
        ]
        return self.data_science.get_window_by_multi_config(config_ids)

    def get_verkehrsmenge_by_multi_config(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsmengen of multiple configs by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsmengen of multiple configs"""
        config_ids = [
            UUID(x) for x in param.replace(")", "").replace("(", "").split("|")
        ]
        return self.data_science.get_verkehrsmenge_by_multi_config(config_ids)

    def get_verkehrsleistung_by_multi_config(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung of multiple configs by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung of multiple configs"""
        config_ids = [
            UUID(x) for x in param.replace(")", "").replace("(", "").split("|")
        ]
        return self.data_science.get_verkehrsleistung_by_multi_config(config_ids)

    # -- FINDERS

    def get_all_station_ids(self, _) -> list[str]:
        """Returns all station ids
        :param _: ignored input time range
        :return: list of all station ids
        """
        return self.data_science.get_all_stations()

    def get_all_train_ids(self, _) -> list[str]:
        """Returns all train ids
        :param _: ignored input time range
        :return: list of all train ids"""
        return self.data_science.get_all_trains()

    def get_all_run_ids(self, _) -> list[UUID]:
        """Returns all run ids
        :param _: ignored input time range
        :return: list of all run ids"""
        return self.data_science.get_all_run_ids()

    def get_all_config_ids(self, _) -> list[UUID]:
        """Returns all config ids
        :param _: ignored input time range
        :return: list of all config ids"""
        return self.data_science.get_all_config_ids()

    def search(self, _) -> list[str]:
        """Returns all grafana functions
        :param _: ignored input time range
        :return: list of all grafana functions"""
        return [
            "get_faults_by_run_id:${run_id}",
            "get_verkehrsleistung_time_by_run_id:${run_id}",
            "get_verkehrsleistung_momentarily_time_by_run_id:${run_id}",
            "get_coal_demand_by_run_id:${run_id}",
            "test_get_spawn_events_by_run_id:${run_id}",
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


def define_and_register_data():
    """Registers all grafana functions"""
    grafana_data_registrator = GrafanaDataRegistrator()

    dg.add_annotation_reader(
        "get_faults_by_run_id", grafana_data_registrator.get_faults_by_run_id
    )
    dg.add_annotation_reader(
        "test_get_spawn_events_by_run_id",
        grafana_data_registrator.get_spawn_events_by_run_id,
    )
    dg.add_metric_reader(
        "get_faults_by_run_id", grafana_data_registrator.get_faults_by_run_id
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_time_by_run_id",
        grafana_data_registrator.get_verkehrsleistung_time_by_run_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_momentarily_time_by_run_id",
        grafana_data_registrator.get_verkehrsleistung_momentarily_time_by_run_id,
    )
    dg.add_metric_reader(
        "get_coal_demand_by_run_id",
        grafana_data_registrator.get_coal_demand_by_run_id,
    )
    dg.add_metric_reader(
        "get_verkehrsmenge_by_run_id",
        grafana_data_registrator.get_verkehrsmenge_by_run_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_by_run_id",
        grafana_data_registrator.get_verkehrsleistung_by_run_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_time_by_config_id",
        grafana_data_registrator.get_verkehrsleistung_time_by_config_id,
    )
    dg.add_metric_reader(
        "get_window_by_config_id", grafana_data_registrator.get_window_by_config_id
    )
    dg.add_metric_reader(
        "get_window_all_by_config_id",
        grafana_data_registrator.get_window_all_by_config_id,
    )
    dg.add_metric_reader(
        "get_verkehrsmenge_by_config_id",
        grafana_data_registrator.get_verkehrsmenge_by_config_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_by_config_id",
        grafana_data_registrator.get_verkehrsleistung_by_config_id,
    )
    dg.add_metric_reader(
        "get_window_by_multi_config",
        grafana_data_registrator.get_window_by_multi_config,
    )
    dg.add_metric_reader(
        "get_verkehrsmenge_by_multi_config",
        grafana_data_registrator.get_verkehrsmenge_by_multi_config,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_by_multi_config",
        grafana_data_registrator.get_verkehrsleistung_by_multi_config,
    )

    dg.add_metric_finder(
        "get_all_station_ids", grafana_data_registrator.get_all_station_ids
    )
    dg.add_metric_finder(
        "get_all_train_ids", grafana_data_registrator.get_all_train_ids
    )
    dg.add_metric_finder("get_all_run_ids", grafana_data_registrator.get_all_run_ids)
    dg.add_metric_finder(
        "get_all_config_ids", grafana_data_registrator.get_all_config_ids
    )
    dg.add_metric_finder("get", grafana_data_registrator.search)
