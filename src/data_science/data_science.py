from uuid import UUID

import numpy as np
import pandas as pd

from src.implementor.models import Run
from src.logger.log_collector import LogCollector


# pylint: disable=too-many-public-methods
class DataScience:
    """The DataScience class is used to get data from the log_collector and to perform data science
    operations on it."""

    log_collector: LogCollector
    unix_2020: int = 1577836800

    def __init__(self):
        """Constructor of DataScience"""
        self.log_collector = LogCollector()

    # -- HELPERS

    def get_all_stations(self) -> list[str]:
        """Returns all stations as a list of strings
        :return: list of stations
        """
        return self.log_collector.get_stations()

    def get_all_trains(self) -> list[str]:
        """Returns all trains as a list of strings
        :return: list of trains
        """
        return self.log_collector.get_trains()

    def get_all_run_ids(self) -> list[UUID]:
        """Returns all run ids as a list of UUIDs
        :return: list of run ids
        """
        return self.log_collector.get_run_ids()

    def get_all_config_ids(self) -> list[UUID]:
        """Returns all config ids as a list of UUIDs
        :return: list of config ids
        """
        return self.log_collector.get_config_ids()

    def _get_window_size_from_values_threshold(
        self, values: pd.Series, threshold
    ) -> float:
        """Returns the window size of a given series of values and a threshold
        :param values: series of values
        :param threshold: percentage of values that have to be included into calculating the result
        :return: window size
        """
        values.dropna(inplace=True)
        if len(values) <= 1:
            return 0
        sorted_values = np.sort(values)
        value_count = len(values)
        threshold_count = int(value_count * threshold)
        min_window_size = sorted_values[threshold_count] - sorted_values[0]
        for i in range(0, value_count - threshold_count):
            min_window_size = min(
                min_window_size, sorted_values[i + threshold_count] - sorted_values[i]
            )
        return min_window_size

    # -- RUN BASED

    # --- TIME

    def get_faults_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns a dataframe of all faults of a given run id
        :param run_id: the run id
        :return: a dataframe of faults
        """
        faults_df = self.log_collector.get_faults(run_id)
        faults_df["begin_time"] = faults_df["begin_tick"].apply(
            lambda x: x + self.unix_2020
        )
        faults_df["begin_time"] = faults_df["begin_time"].apply(
            pd.to_datetime, unit="s"
        )
        faults_df["end_time"] = faults_df["end_tick"].apply(
            lambda x: x + self.unix_2020
        )
        faults_df["end_time"] = faults_df["end_time"].apply(pd.to_datetime, unit="s")
        faults_df.set_index("begin_time", inplace=True)
        faults_df["fault_id"] = faults_df["fault_id"].astype("string")

        faults_df["title"] = faults_df["fault_type"].apply(
            lambda x: " ".join(x.split("_")).capitalize()
        )
        return faults_df

    def _get_interpolate_passed_section_length_by_tick(
        self,
        enter_tick: int,
        leave_tick: int,
        block_section_length: float,
        current_tick: int,
    ) -> float:
        """Returns the fraction length of a block section that has been passed until a given tick
        :param enter_tick: enter tick
        :param leave_tick: leave tick
        :param block_section_length: block_section_length
        :param current_tick: current tick
        :return: block section length
        """
        if current_tick > leave_tick:
            return block_section_length
        return (
            block_section_length
            * (current_tick - enter_tick)
            / (leave_tick - enter_tick)
        )

    def _calculate_verkehrsleistung_by_tick(
        self, block_section_times_df: pd.DataFrame, tick: int, start_tick: int
    ) -> float:
        """Returns the verkehrsleistung by a given tick
        :param block_section_times_df: dataframe of block section times
        :param tick: tick
        :param start_tick: start tick
        :return: verkehrsleistung
        """
        source_df = block_section_times_df.drop(
            block_section_times_df[block_section_times_df["enter_tick"] > tick].index
        )
        source_df["dist"] = source_df.apply(
            lambda row: self._get_interpolate_passed_section_length_by_tick(
                row["enter_tick"], row["leave_tick"], row["block_section_length"], tick
            ),
            axis=1,
        )
        if tick == start_tick:
            return 0
        return source_df["dist"].sum() * 3600 / (tick - start_tick)

    def get_verkehrsleistung_time_by_run_id(
        self, run_id: UUID, delta_tick=10
    ) -> pd.DataFrame:
        """Returns the accumulated verkehrsleistung over a period of time by a given run id
        :param run_id: the run id
        :param delta_tick: delta tick
        :return: dataframe of verkehrsleistung
        """
        block_section_times_df = self.log_collector.get_block_section_times_all_trains(
            run_id
        )
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        verkehrsleistung_df = pd.DataFrame(
            {
                "tick": np.arange(
                    block_section_times_df["enter_tick"].min(),
                    block_section_times_df["leave_tick"].max() + 1,
                    delta_tick,
                )
            }
        )
        verkehrsleistung_df["verkehrsleistung"] = verkehrsleistung_df.apply(
            lambda row: self._calculate_verkehrsleistung_by_tick(
                block_section_times_df,
                row["tick"],
                block_section_times_df["enter_tick"].min(),
            ),
            axis=1,
        )
        verkehrsleistung_df["time"] = verkehrsleistung_df["tick"].apply(
            lambda x: x + self.unix_2020
        )
        verkehrsleistung_df["time"] = verkehrsleistung_df["time"].apply(
            pd.to_datetime, unit="s"
        )
        verkehrsleistung_df.set_index("time", inplace=True)
        del verkehrsleistung_df["tick"]
        return verkehrsleistung_df

    def _get_section_length_momentarily_by_tick(
        self,
        enter_tick: int,
        leave_tick: int,
        block_section_length: float,
        current_tick: int,
        delta_tick: int,
    ) -> float:
        """Returns the fraction length of a block section that has been passed until a given tick
        for the duration of delta_tick
        :param enter_tick: enter tick
        :param leave_tick: leave tick
        :param block_section_length: block_section_length
        :param current_tick: current tick
        :param delta_tick: delta tick
        :return: block section length
        """
        max_edge = np.minimum(leave_tick, current_tick)
        min_edge = np.maximum(enter_tick, current_tick - delta_tick)
        return block_section_length * (max_edge - min_edge) / (leave_tick - enter_tick)

    def _calculate_verkehrsleistung_momentarily_by_tick(
        self, block_section_times_df: pd.DataFrame, tick: int, delta_tick: int
    ) -> float:
        """Returns the verkehrsleistung by a given tick for the duration of delta_tick
        :param block_section_times_df: dataframe of block section times
        :param tick: tick
        :param delta_tick: delta tick
        :return: verkehrsleistung
        """

        source_df = block_section_times_df.loc[
            (block_section_times_df["leave_tick"] >= tick - delta_tick)
            & (block_section_times_df["enter_tick"] <= tick)
        ]
        source_df["dist"] = self._get_section_length_momentarily_by_tick(
            source_df["enter_tick"],
            source_df["leave_tick"],
            source_df["block_section_length"],
            tick,
            delta_tick,
        )
        return source_df["dist"].sum() * 3600 / delta_tick

    def get_verkehrsleistung_momentarily_time_by_run_id(
        self, run_id: UUID, delta_tick=10
    ) -> pd.DataFrame:
        """Returns the momentary verkehrsleistung over a period of time by a given run id
        :param run_id: the run id
        :param delta_tick: delta tick
        :return: dataframe of verkehrsleistung
        """

        block_section_times_df = self.log_collector.get_block_section_times_all_trains(
            run_id
        )
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        verkehrsleistung_df = pd.DataFrame(
            {
                "tick": np.arange(
                    block_section_times_df["enter_tick"].min(),
                    block_section_times_df["leave_tick"].max() + 1,
                    delta_tick,
                )
            }
        )
        verkehrsleistung_df["verkehrsleistung"] = verkehrsleistung_df.apply(
            lambda row: self._calculate_verkehrsleistung_momentarily_by_tick(
                block_section_times_df, row["tick"], delta_tick=delta_tick
            ),
            axis=1,
        )

        verkehrsleistung_df["time"] = verkehrsleistung_df["tick"] + self.unix_2020
        verkehrsleistung_df["time"] = pd.to_datetime(
            verkehrsleistung_df["time"], unit="s"
        )
        verkehrsleistung_df.set_index("time", inplace=True)
        del verkehrsleistung_df["tick"]
        return verkehrsleistung_df

    def get_coal_demand_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns the coal demand by a given run id
        :param run_id: run id
        :return: dataframe of coal demand
        """
        raise NotImplementedError()

    def get_spawn_events_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns the spawn events by a given run id
        :param run_id: run id
        :return: dataframe of spawn events
        """
        raise NotImplementedError()

    # --- SCALARS
    def get_verkehrsmenge_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns the verkehrsmenge by a given run id
        :param run_id: run id
        :return: dataframe of verkehrsmenge
        """

        block_section_times_df = self.log_collector.get_block_section_times_all_trains(
            run_id
        )
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = pd.DataFrame(
            {
                "verkehrsmenge": [block_section_times_df["block_section_length"].sum()],
            }
        )
        return grouped_df

    def get_verkehrsleistung_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns the verkehrsleistung by a given run id
        :param run_id: run id
        :return: dataframe of verkehrsleistung
        """
        block_section_times_df = self.log_collector.get_block_section_times_all_trains(
            run_id
        )
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = pd.DataFrame(
            {
                "enter_tick": [block_section_times_df["enter_tick"].min()],
                "leave_tick": [block_section_times_df["leave_tick"].max()],
                "block_section_length": [
                    block_section_times_df["block_section_length"].sum()
                ],
            }
        )

        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"]
            * 3600
            / (row["leave_tick"] - row["enter_tick"]),
            axis=1,
        )
        return grouped_df

    # --- MAP

    def get_station_counts_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns the station counts by a given run id
        :param run_id: run id
        :return: dataframe of station counts
        """
        raise NotImplementedError()

    # -- CONFIG BASED

    # --- TIME

    def get_window_time_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the window time by a given config id
        :param config_id: config id
        :return: dataframe of window time"""

        raise NotImplementedError()

    def _calculate_verkehrsleistung_momentarily_by_tick_multiple_runs(
        self, block_section_times_df: pd.DataFrame, tick: int, delta_tick: int
    ) -> float:
        """Calculates the verkehrsleistung momentarily by a given tick
        :param block_section_times_df: dataframe of block section times
        :param tick: tick
        :param delta_tick: delta tick
        :return: verkehrsleistung momentarily
        """

        verkehrsleistung = []
        for run_id in block_section_times_df["run_id"].unique():
            source_df = block_section_times_df[
                block_section_times_df["run_id"] == run_id
            ]
            verkehrsleistung.append(
                self._calculate_verkehrsleistung_momentarily_by_tick(
                    source_df, tick, delta_tick
                )
            )
        return np.array(verkehrsleistung).mean()

    def get_verkehrsleistung_time_by_config_id(
        self, config_id: UUID, delta_tick=10
    ) -> pd.DataFrame:
        """Returns the verkehrsleistung time by a given config id
        :param config_id: config id
        :param delta_tick: delta tick
        :return: dataframe of verkehrsleistung time
        """
        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["run_id"] = run_id.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        verkehrsleistung_df = pd.DataFrame(
            {
                "tick": np.arange(
                    block_section_times_df["enter_tick"].min(),
                    block_section_times_df["leave_tick"].max() + 1,
                    delta_tick,
                )
            }
        )
        verkehrsleistung_df["verkehrsleistung"] = verkehrsleistung_df.apply(
            lambda row: self._calculate_verkehrsleistung_momentarily_by_tick_multiple_runs(
                block_section_times_df, row["tick"], delta_tick
            ),
            axis=1,
        )
        verkehrsleistung_df["time"] = verkehrsleistung_df["tick"].apply(
            lambda x: x + self.unix_2020
        )
        verkehrsleistung_df["time"] = verkehrsleistung_df["time"].apply(
            pd.to_datetime, unit="s"
        )
        verkehrsleistung_df.set_index("time", inplace=True)
        del verkehrsleistung_df["tick"]
        return verkehrsleistung_df

    def get_coal_demand_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the coal demand by a given config id
        :param config_id: config id
        :return: coal demand dataframe
        """
        raise NotImplementedError()

    def get_spawn_events_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the spawn events by a given config id
        :param config_id: config id
        :return: spawn events dataframe
        """
        raise NotImplementedError()

    # --- SCALAR

    def get_window_by_config_id(self, config_id: UUID, threshold=0.9) -> pd.DataFrame:
        """Returns the spawn and departure windows by config id
        :param config_id: config id
        :param threshold: percentage of values that have to be included into calculating the result
        :return: window size dataframe
        """

        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            departures_arrivals_df = (
                self.log_collector.get_departures_arrivals_all_trains(run_id)
            )
            departures_arrivals_df["run_id"] = run_id.id
            df_list.append(departures_arrivals_df)
        departures_arrivals_df = pd.concat(df_list, axis=0)
        out_df = departures_arrivals_df[
            ["station_id", "train_id", "arrival_tick", "departure_tick"]
        ]
        out_df = out_df.groupby(["station_id", "train_id"]).agg(
            lambda x: self._get_window_size_from_values_threshold(x, threshold)
        )
        out_df.reset_index(inplace=True)
        del out_df["station_id"]
        del out_df["train_id"]
        out_df = list(out_df.mean())
        out_df = pd.DataFrame(
            {"arrival_tick": [out_df[0]], "departure_tick": [out_df[1]]}
        )

        return out_df

    def get_window_all_by_config_id(
        self, config_id: UUID, threshold=0.9
    ) -> pd.DataFrame:
        """Returns the window for all trains and stations by config id
        :param config_id: config id
        :param threshold: percentage of values that have to be included into calculating the result
        :return: window dataframe
        """
        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            departures_arrivals_df = (
                self.log_collector.get_departures_arrivals_all_trains(run_id)
            )
            departures_arrivals_df["run_id"] = run_id.id
            df_list.append(departures_arrivals_df)
        departures_arrivals_df = pd.concat(df_list, axis=0)
        out_df = departures_arrivals_df[
            ["station_id", "train_id", "arrival_tick", "departure_tick"]
        ]
        out_df = out_df.groupby(["station_id", "train_id"]).agg(
            lambda x: self._get_window_size_from_values_threshold(x, threshold)
        )
        out_df.reset_index(inplace=True)
        return out_df

    def get_verkehrsmenge_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the verkehrsmenge by a given config id
        :param config_id: config id
        :return: verkehrsmenge dataframe
        """

        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["run_id"] = run_id.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby("run_id").agg(
            {"enter_tick": "min", "leave_tick": "max", "block_section_length": "sum"}
        )
        grouped_df["enter_tick"] = grouped_df["enter_tick"].astype("Int64")
        grouped_df["leave_tick"] = grouped_df["leave_tick"].astype("Int64")
        return grouped_df

    def get_verkehrsleistung_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the verkehrsleistung by a given config id
        :param config_id: config id
        :return: verkehrsleistung dataframe
        """
        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["run_id"] = run_id.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby("run_id").agg(
            {"enter_tick": "min", "leave_tick": "max", "block_section_length": "sum"}
        )
        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"]
            * 3600
            / (row["leave_tick"] - row["enter_tick"]),
            axis=1,
        )
        grouped_df["enter_tick"] = grouped_df["enter_tick"].astype("Int64")
        grouped_df["leave_tick"] = grouped_df["leave_tick"].astype("Int64")
        return grouped_df

    # -- MULTI CONFIG BASED

    # --- SCALAR

    def get_window_by_multi_config(
        self, config_id_list: list[UUID], threshold=0.9
    ) -> pd.DataFrame:
        """Returns the window sizes of given configs
        :param config_id_list: list of config ids
        :param threshold: percentage of values that have to be included into calculating the result
        :return: window size dataframe
        """
        df_list = []
        for run_id in Run.select().where(
            Run.simulation_configuration << config_id_list
        ):
            departures_arrivals_df = (
                self.log_collector.get_departures_arrivals_all_trains(run_id)
            )
            departures_arrivals_df["run_id"] = run_id.id
            departures_arrivals_df["config_id"] = run_id.simulation_configuration.id
            df_list.append(departures_arrivals_df)
        departures_arrivals_df = pd.concat(df_list, axis=0)
        out_df = departures_arrivals_df[
            ["config_id", "station_id", "train_id", "arrival_tick", "departure_tick"]
        ]
        out_df = out_df.groupby(["config_id", "station_id", "train_id"]).agg(
            lambda x: self._get_window_size_from_values_threshold(x, threshold)
        )
        out_df = out_df.groupby("config_id").mean()
        out_df.reset_index(inplace=True)
        return out_df

    def get_verkehrsmenge_by_multi_config(
        self, config_id_list: list[UUID]
    ) -> pd.DataFrame:
        """Returns the verkehrsmenge of given configs
        :param config_id_list: list of simulation configuration ids
        :return: dataframe of verkehrsmenge
        """
        df_list = []
        for run_id in Run.select().where(
            Run.simulation_configuration << config_id_list
        ):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["run_id"] = run_id.id
            block_section_times_df["config_id"] = run_id.simulation_configuration.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby(["config_id", "run_id"]).agg(
            {"enter_tick": "min", "leave_tick": "max", "block_section_length": "sum"}
        )
        grouped_df = grouped_df.groupby("config_id").agg(
            {"block_section_length": "mean"}
        )
        grouped_df.reset_index(inplace=True)
        return grouped_df

    def get_verkehrsleistung_by_multi_config(
        self, config_id_list: list[UUID]
    ) -> pd.DataFrame:
        """Returns the verkehrsleistung of given list of configs
        :param config_id_list: list of simulation configurations
        :return: dataframe of verkehrsleistung
        """
        df_list = []
        for run_id in Run.select().where(
            Run.simulation_configuration << config_id_list
        ):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["run_id"] = run_id.id
            block_section_times_df["config_id"] = run_id.simulation_configuration.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby(["config_id", "run_id"]).agg(
            {"enter_tick": "min", "leave_tick": "max", "block_section_length": "sum"}
        )
        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"]
            * 3600
            / (row["leave_tick"] - row["enter_tick"]),
            axis=1,
        )
        grouped_df = grouped_df.groupby("config_id").mean()
        grouped_df.reset_index(inplace=True)
        return grouped_df