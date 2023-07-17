from uuid import UUID

import pandas as pd
from grafana_pandas_datasource.registry import data_generators as dg

from src.data_science.data_science import DataScience
from src.implementor.models import Run, SimulationConfiguration


# pylint: disable=too-many-public-methods
class GrafanaDataRegistrator:
    """Class that encapsulates all functions that are used by grafana"""

    def __init__(self):
        """Constructor of GrafanaDataRegistrator"""
        self.data_science = DataScience()

    # -- METRICS

    # --- RUN

    @staticmethod
    def _get_run_id_from_param(param) -> UUID:
        """Returns a run id from params
        :param param: Grafana params
        :return: run id
        """
        run_id = Run.select(Run.id).where(param == Run.readable_id).get().id
        return run_id

    @staticmethod
    def _get_config_id_from_param(param) -> UUID:
        """Returns a config id from params
        :param param: Grafana params
        :return: config id
        """
        config_id = (
            SimulationConfiguration.select(SimulationConfiguration.id)
            .where(param == SimulationConfiguration.readable_id)
            .get()
            .id
        )
        return config_id

    @staticmethod
    def _get_config_id_list_from_param(param) -> list[UUID]:
        """Returns a list of config ids from params
        :param param: Grafana params
        :return: list of config id
        """
        config_readable_ids = param.replace(")", "").replace("(", "").split("|")
        # pylint will not recognize that peewee results are iterable
        # pylint: disable=not-an-iterable
        config_ids = [
            config_id.id
            for config_id in SimulationConfiguration.select(
                SimulationConfiguration.id
            ).where(SimulationConfiguration.readable_id << config_readable_ids)
        ]
        return config_ids

    def get_faults_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns a list of all faults by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of faults
        """
        run_id = self._get_run_id_from_param(param)
        return self.data_science.get_faults_by_run_id(run_id)
    def get_verkehrsleistung_momentarily_time_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the momentary verkehrsleistung over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung over time"""
        run_id = self._get_run_id_from_param(param)
        return self.data_science.get_verkehrsleistung_momentarily_time_by_run_id(run_id)

    def get_coal_demand_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the coal demand over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of coal demand over time"""
        run_id = self._get_run_id_from_param(param)
        return self.data_science.get_coal_demand_by_run_id(run_id)

    def get_spawn_events_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the train spawn events over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of all train spawn events over time
        """
        run_id = self._get_run_id_from_param(param)
        return self.data_science.get_spawn_events_by_run_id(run_id)

    def get_verkehrsarbeit_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsarbeit by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsarbeit"""
        run_id = self._get_run_id_from_param(param)
        return self.data_science.get_verkehrsarbeit_by_run_id(run_id)

    def get_verkehrsleistung_by_run_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung"""
        run_id = self._get_run_id_from_param(param)
        return self.data_science.get_verkehrsleistung_by_run_id(run_id)

    # --- CONFIG

    def get_window_size_time_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the arrival and departure window sizes over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_window_size_time_by_config_id(config_id)

    def get_verkehrsleistung_time_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung over time"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_verkehrsleistung_time_by_config_id(config_id)

    def get_coal_demand_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the coal demand over time by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of coal demand over time by config id"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_coal_demand_by_config_id(config_id)

    def get_coal_spawn_events_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the coal train spawn events by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of coal train spawn events by config id"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_coal_spawn_events_by_config_id(config_id)

    def get_window_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the window size of the entire network by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of window size"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_window_by_config_id(config_id)

    def get_window_all_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns window sizes of stations and trains by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of window sizes of stations and trains"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_window_all_by_config_id(config_id)

    def get_verkehrsarbeit_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsarbeit by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsarbeit"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_verkehrsarbeit_by_config_id(config_id)

    def get_verkehrsleistung_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_verkehrsleistung_by_config_id(config_id)

    def get_average_verkehrsarbeit_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the average verkehrsarbeit by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of average verkehrsarbeit"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_average_verkehrsarbeit_by_config_id(config_id)

    def get_average_verkehrsleistung_by_config_id(self, param, _) -> pd.DataFrame:
        """Returns the average verkehrsleistung by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of average verkehrsleistung"""
        config_id = self._get_config_id_from_param(param)
        return self.data_science.get_average_verkehrsleistung_by_config_id(config_id)

    # --- MULTI CONFIG

    def get_window_by_multi_config(self, param, _) -> pd.DataFrame:
        """Returns multiple windows by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of multiple windows"""
        config_ids = self._get_config_id_list_from_param(param)
        return self.data_science.get_window_by_multi_config(config_ids)

    def get_verkehrsarbeit_by_multi_config(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsarbeitn of multiple configs by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsarbeitn of multiple configs"""
        config_ids = self._get_config_id_list_from_param(param)
        return self.data_science.get_verkehrsarbeit_by_multi_config(config_ids)

    def get_verkehrsleistung_by_multi_config(self, param, _) -> pd.DataFrame:
        """Returns the verkehrsleistung of multiple configs by grafana params
        :param param: Grafana params
        :param _: ignored input time range
        :return: dataframe of verkehrsleistung of multiple configs"""
        config_ids = self._get_config_id_list_from_param(param)
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

    def get_all_run_ids(self, _) -> list[str]:
        """Returns all run ids
        :param _: ignored input time range
        :return: list of all run ids"""
        return self.data_science.get_all_run_ids()

    def get_all_config_ids(self, _) -> list[str]:
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
            "get_verkehrsleistung_momentarily_time_by_run_id:${run_id}",
            "get_coal_demand_by_run_id:${run_id}",
            "get_spawn_events_by_run_id:${run_id}",
            "get_verkehrsarbeit_by_run_id:${run_id}",
            "get_verkehrsleistung_by_run_id:${run_id}",
            "get_window_size_time_by_config_id:${config_id}",
            "get_verkehrsleistung_time_by_config_id:${config_id}",
            "get_coal_demand_by_config_id:${config_id}",
            "get_coal_spawn_events_by_config_id:${config_id}",
            "get_window_by_config_id:${config_id}",
            "get_window_all_by_config_id:${config_id}",
            "get_verkehrsarbeit_by_config_id:${config_id}",
            "get_verkehrsleistung_by_config_id:${config_id}",
            "get_average_verkehrsarbeit_by_config_id:${config_id}",
            "get_average_verkehrsleistung_by_config_id:${config_id}",
            "get_window_by_multi_config:${config_ids}",
            "get_verkehrsarbeit_by_multi_config:${config_ids}",
            "get_verkehrsleistung_by_multi_config:${config_ids}",
        ]


def define_and_register_data():
    """Registers all grafana functions"""
    grafana_data_registrator = GrafanaDataRegistrator()

    dg.add_annotation_reader(
        "get_faults_by_run_id", grafana_data_registrator.get_faults_by_run_id
    )
    dg.add_annotation_reader(
        "get_spawn_events_by_run_id",
        grafana_data_registrator.get_spawn_events_by_run_id,
    )
    dg.add_annotation_reader(
        "get_coal_spawn_events_by_config_id",
        grafana_data_registrator.get_coal_spawn_events_by_config_id,
    )
    dg.add_metric_reader(
        "get_faults_by_run_id", grafana_data_registrator.get_faults_by_run_id
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
        "get_verkehrsarbeit_by_run_id",
        grafana_data_registrator.get_verkehrsarbeit_by_run_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_by_run_id",
        grafana_data_registrator.get_verkehrsleistung_by_run_id,
    )
    dg.add_metric_reader(
        "get_window_size_time_by_config_id",
        grafana_data_registrator.get_window_size_time_by_config_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_time_by_config_id",
        grafana_data_registrator.get_verkehrsleistung_time_by_config_id,
    )
    dg.add_metric_reader(
        "get_coal_demand_by_config_id",
        grafana_data_registrator.get_coal_demand_by_config_id,
    )
    dg.add_metric_reader(
        "get_window_by_config_id", grafana_data_registrator.get_window_by_config_id
    )
    dg.add_metric_reader(
        "get_window_all_by_config_id",
        grafana_data_registrator.get_window_all_by_config_id,
    )
    dg.add_metric_reader(
        "get_verkehrsarbeit_by_config_id",
        grafana_data_registrator.get_verkehrsarbeit_by_config_id,
    )
    dg.add_metric_reader(
        "get_verkehrsleistung_by_config_id",
        grafana_data_registrator.get_verkehrsleistung_by_config_id,
    )
    dg.add_metric_reader(
        "get_average_verkehrsarbeit_by_config_id",
        grafana_data_registrator.get_average_verkehrsarbeit_by_config_id,
    )
    dg.add_metric_reader(
        "get_average_verkehrsleistung_by_config_id",
        grafana_data_registrator.get_average_verkehrsleistung_by_config_id,
    )
    dg.add_metric_reader(
        "get_window_by_multi_config",
        grafana_data_registrator.get_window_by_multi_config,
    )
    dg.add_metric_reader(
        "get_verkehrsarbeit_by_multi_config",
        grafana_data_registrator.get_verkehrsarbeit_by_multi_config,
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
