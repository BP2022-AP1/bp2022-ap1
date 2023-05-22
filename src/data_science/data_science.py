from datetime import timedelta
from uuid import UUID

import numpy as np
import pandas as pd
from pandas import Series

from src.implementor.models import Run
from src.logger.log_collector import LogCollector
from src.schedule.demand_schedule_strategy import DemandScheduleStrategy
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.smard_api import SmardApi
from src.spawner.spawner import (
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)


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
                    0,
                    block_section_times_df["leave_tick"].max() + 1,
                    delta_tick,
                )
            }
        )
        verkehrsleistung_df["verkehrsleistung"] = verkehrsleistung_df.apply(
            lambda row: self._calculate_verkehrsleistung_by_tick(
                block_section_times_df,
                row["tick"],
                0,
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
        dist_series = self._get_section_length_momentarily_by_tick(
            source_df["enter_tick"],
            source_df["leave_tick"],
            source_df["block_section_length"],
            tick,
            delta_tick,
        )
        return np.sum(dist_series) * 3600 / delta_tick

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
                    0,
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
        simulation_configuration = (
            Run.select().where(Run.id == run_id).get().simulation_configuration
        )
        return self.get_coal_demand_by_config_id(simulation_configuration)

    def get_spawn_events_by_run_id(self, run_id: UUID) -> pd.DataFrame:
        """Returns the spawn events by a given run id
        :param run_id: run id
        :return: dataframe of spawn events
        """
        spawn_df = self.log_collector.get_train_spawn_times(run_id)
        spawn_df["time"] = spawn_df["tick"] + self.unix_2020
        spawn_df["time"] = pd.to_datetime(spawn_df["time"], unit="s")
        spawn_df["title"] = f"Spawn train {spawn_df['train_id']}"
        spawn_df["title"] = spawn_df["train_id"].apply(lambda e: f"Spawn train {e}")
        spawn_df.set_index("time", inplace=True)
        del spawn_df["tick"]
        del spawn_df["train_id"]
        return spawn_df

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
        block_section_times_df["train_type"] = block_section_times_df["train_id"].apply(
            lambda train_id: train_id.split("_")[2])
        grouped_df = block_section_times_df.groupby("train_type").apply(
            lambda data: pd.Series(
                {
                    "verkehrsmenge": data["block_section_length"].sum(),
                }
            )
        )
        grouped_df.reset_index(inplace=True)
        all_df = pd.DataFrame(
            {
                "train_type": ["all"],
                "verkehrsmenge": [grouped_df["verkehrsmenge"].sum()],
            }
        )
        grouped_df = pd.concat(
            [grouped_df, all_df],
            ignore_index=True,
        )
        print('grouped_df', grouped_df)
        print('all_df', all_df)
        grouped_df.reset_index(inplace=True)
        del grouped_df["index"]
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
        block_section_times_df["train_type"] = block_section_times_df['train_id'].apply(
            lambda train_id: train_id.split('_')[2])

        grouped_df = block_section_times_df.groupby("train_type").apply(
            lambda data: pd.Series({
                "enter_tick": 0,
                "leave_tick": data["leave_tick"].max(),
                "block_section_length": data["block_section_length"].sum(),
            })
        )

        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"]
            * 3600
            / (row["leave_tick"] - row["enter_tick"]),
            axis=1,
        )
        grouped_df["enter_tick"] = grouped_df["enter_tick"].astype("Int64")
        grouped_df["leave_tick"] = grouped_df["leave_tick"].astype("Int64")
        grouped_df.reset_index(inplace=True)
        all_df = pd.DataFrame(
            {
                "train_type": ["all"],
                "enter_tick": [0],
                "leave_tick": [grouped_df["leave_tick"].max()],
                "block_section_length": [grouped_df["block_section_length"].sum()],
                "verkehrsleistung": [grouped_df["verkehrsleistung"].sum()],
            }
        )

        grouped_df = pd.concat(
            [grouped_df, all_df],
            ignore_index=True,
        )
        print('grouped_df', grouped_df)
        print('all_df', all_df)
        grouped_df.reset_index(inplace=True)
        del grouped_df["index"]
        with pd.option_context('display.max_rows', None,
                               'display.max_columns', None,
                               'display.precision', 3,
                               ):
            print('grouped_df', grouped_df)
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

    def _get_window_size_by_tick_config_id(
        self, departures_arrivals_df: pd.DataFrame, tick: int, threshold=0.9
    ) -> Series:
        """Returns the arrival and departure window sizes by a given tick and config id
        :param departures_arrivals_df: dataframe containing departure and arrival times
        :param tick: current tick
        :param threshold: threshold used to compute departure and arrival time windows
        :return: dataframe of window size"""

        out_df = departures_arrivals_df[
            ["station_id", "train_id", "arrival_tick", "departure_tick"]
        ]
        out_df = out_df[
            (out_df["arrival_tick"] <= tick) | (out_df["departure_tick"] <= tick)
        ]
        out_df.loc[out_df["arrival_tick"] > tick, "arrival_tick"] = None
        out_df.loc[out_df["departure_tick"] > tick, "departure_tick"] = None

        out_df = out_df.groupby(["station_id", "train_id"]).agg(
            lambda x: self._get_window_size_from_values_threshold(x, threshold)
        )
        if out_df.empty:
            return pd.Series([0.0, 0.0])
        out_df.reset_index(inplace=True)
        del out_df["station_id"]
        del out_df["train_id"]
        out_df = list(out_df.mean())
        out_df = pd.Series([out_df[0], out_df[1]])
        return out_df

    def get_window_size_time_by_config_id(
        self, config_id: UUID, delta_tick=10
    ) -> pd.DataFrame:
        """Returns the arrival and departure window sizes over time by a given config id
        :param config_id: config id
        :return: dataframe of window size"""
        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            departures_arrivals_df = (
                self.log_collector.get_departures_arrivals_all_trains(run_id)
            )
            departures_arrivals_df["run_id"] = run_id.id
            df_list.append(departures_arrivals_df)
        departures_arrivals_df = pd.concat(df_list, axis=0)
        window_size_df = pd.DataFrame(
            {
                "tick": np.arange(
                    0,
                    np.maximum(
                        departures_arrivals_df["arrival_tick"].max(),
                        departures_arrivals_df["departure_tick"].max(),
                    ),
                    delta_tick,
                )
            }
        )
        result_df = window_size_df["tick"].apply(
            lambda tick: self._get_window_size_by_tick_config_id(
                departures_arrivals_df, tick
            )
        )

        window_size_df.loc[:, "arrival_size"] = result_df.iloc[:, 0]
        window_size_df.loc[:, "departure_size"] = result_df.iloc[:, 1]
        window_size_df["time"] = window_size_df["tick"].apply(
            lambda x: x + self.unix_2020
        )
        window_size_df["time"] = window_size_df["time"].apply(pd.to_datetime, unit="s")
        window_size_df.set_index("time", inplace=True)
        del window_size_df["tick"]
        return window_size_df

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
                    0,
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

    def _get_demand_schedule_strategies_by_config_id(
        self, config_id: UUID
    ) -> list[tuple[DemandScheduleStrategy, UUID]]:
        """Returns the demand schedule strategies by a given config id
        :param config_id: config id
        :return: list of demand schedule strategies
        """
        spawner_configurations = list(
            SpawnerConfigurationXSimulationConfiguration.select().where(
                SpawnerConfigurationXSimulationConfiguration.simulation_configuration
                == config_id
            )
        )
        schedule_configurations = [
            [
                config.schedule_configuration_id
                for config in SpawnerConfigurationXSchedule.select().where(
                    SpawnerConfigurationXSchedule.spawner_configuration_id
                    == spawner_config.spawner_configuration_id
                )
            ]
            for spawner_config in spawner_configurations
        ]
        schedule_configurations = [
            item for sublist in schedule_configurations for item in sublist
        ]
        demand_schedule_strategies_configurations = list(
            ScheduleConfiguration.select().where(
                (ScheduleConfiguration.id << schedule_configurations)
                & (ScheduleConfiguration.strategy_type == "DemandScheduleStrategy")
            )
        )
        demand_schedule_strategies = [
            (DemandScheduleStrategy.from_schedule_configuration(config), config.id)
            for config in demand_schedule_strategies_configurations
        ]
        return demand_schedule_strategies

    def get_coal_demand_by_config_id(
        self, simulation_configuration: UUID
    ) -> pd.DataFrame:
        """Returns the coal demand by a given config id
        :param config_id: config id
        :return: coal demand dataframe
        """
        demand_schedule_strategies = self._get_demand_schedule_strategies_by_config_id(
            simulation_configuration
        )
        smard_api = SmardApi()
        dataframes = []
        for strategy, config_id in demand_schedule_strategies:
            data = [
                entry.value
                for entry in smard_api.get_data(
                    strategy.start_datetime,
                    strategy.start_datetime
                    + timedelta(seconds=strategy.end_tick - strategy.start_tick),
                )
            ]
            data = map(strategy.compute_coal_consumption, data)
            smard_df = pd.DataFrame(data, columns=[f"value_{config_id}"])

            smard_df["tick"] = pd.Series(
                range(strategy.start_tick, strategy.end_tick + 1, 900), dtype="int64"
            )
            smard_df.set_index("tick", inplace=True)

            dataframes.append(smard_df)

        result_df = pd.concat(dataframes)
        result_df.reset_index(inplace=True)
        result_df["time"] = result_df["tick"] + self.unix_2020
        result_df["time"] = pd.to_datetime(result_df["time"], unit="s")
        result_df.set_index("time", inplace=True)
        del result_df["tick"]
        return result_df

    def get_coal_spawn_events_by_config_id(
        self, simulation_configuration: UUID
    ) -> pd.DataFrame:
        """Returns the spawn events by a given config id
        :param config_id: config id
        :return: spawn events dataframe
        """
        demand_schedule_strategies = self._get_demand_schedule_strategies_by_config_id(
            simulation_configuration
        )
        dataframes = []
        for strategy, config_id in demand_schedule_strategies:
            spawn_df = pd.DataFrame({"tick": strategy.spawn_ticks})
            spawn_df["title"] = f"Spawn train from config {config_id}"
            spawn_df["time"] = spawn_df["tick"] + self.unix_2020
            spawn_df["time"] = pd.to_datetime(spawn_df["time"], unit="s")

            dataframes.append(spawn_df)

        result_df = pd.concat(dataframes)
        result_df.reset_index(inplace=True)
        result_df.set_index("time", inplace=True)
        del result_df["tick"]
        del result_df["index"]
        return result_df

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
            departures_arrivals_df["train_type"] = departures_arrivals_df["train_id"].apply(
                lambda train_id: train_id.split("_")[2]
            )
            departures_arrivals_df["run_id"] = run_id.id
            df_list.append(departures_arrivals_df)
        departures_arrivals_df = pd.concat(df_list, axis=0)
        out_df = departures_arrivals_df[
            ["station_id", "train_id", "train_type", "arrival_tick", "departure_tick"]
        ]
        all_df = out_df.groupby(["station_id", "train_id"]).apply(
            lambda data: pd.Series(
                {
                    "train_type": "all",
                    "arrival_tick": self._get_window_size_from_values_threshold(data["arrival_tick"], threshold),
                    "departure_tick": self._get_window_size_from_values_threshold(data["departure_tick"], threshold),
                }
            )
        )

        all_df.reset_index(inplace=True)
        del all_df["station_id"]
        del all_df["train_id"]
        out_df = out_df.groupby(["station_id", "train_id", "train_type"]).agg(
            lambda x: self._get_window_size_from_values_threshold(x, threshold)
        )
        out_df.reset_index(inplace=True)
        del out_df["station_id"]
        del out_df["train_id"]
        out_df = pd.concat([out_df, all_df], axis=0)
        out_df = out_df.groupby("train_type").apply(
            lambda data: pd.Series(
                {
                    "arrival_tick": data["arrival_tick"].mean(),
                    "departure_tick": data["departure_tick"].mean(),
                }
            )
        )
        out_df.reset_index(inplace=True)
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
            {"leave_tick": "max", "block_section_length": "sum"}
        )
        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"] * 3600 / row["leave_tick"],
            axis=1,
        )
        grouped_df["leave_tick"] = grouped_df["leave_tick"].astype("Int64")
        return grouped_df

    def get_average_verkehrsmenge_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the average verkehrsmenge by a given config id
        :param config_id: config id
        :return: verkehrsmenge dataframe
        """

        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["train_type"] = block_section_times_df["train_id"].apply(
                lambda train_id: train_id.split("_")[2])
            block_section_times_df["run_id"] = run_id.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby(["run_id", "train_type"]).apply(
            lambda data: pd.Series(
                {
                    "verkehrsmenge": data["block_section_length"].sum(),
                }
            )
        )
        grouped_df.reset_index(inplace=True)
        all_df = grouped_df.groupby("run_id").apply(
            lambda data: pd.Series(
                {
                    "train_type": "all",
                    "verkehrsmenge": data["verkehrsmenge"].sum(),
                }
            )
        )
        all_df.reset_index(inplace=True)
        grouped_df = pd.concat([grouped_df, all_df], axis=0)
        grouped_df = grouped_df.groupby(["train_type"]).agg(
            {"verkehrsmenge": "mean"}
        )
        grouped_df.reset_index(inplace=True)
        return grouped_df

    def get_average_verkehrsleistung_by_config_id(self, config_id: UUID) -> pd.DataFrame:
        """Returns the average verkehrsleistung by a given config id
        :param config_id: config id
        :return: verkehrsleistung dataframe"""
        df_list = []
        for run_id in Run.select().where(Run.simulation_configuration == config_id):
            block_section_times_df = (
                self.log_collector.get_block_section_times_all_trains(run_id)
            )
            block_section_times_df["train_type"] = block_section_times_df["train_id"].apply(
                lambda train_id: train_id.split("_")[2])
            block_section_times_df["run_id"] = run_id.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby(["run_id", "train_type"]).apply(
            lambda data: pd.Series(
                {
                    "enter_tick": 0,
                    "leave_tick": data["leave_tick"].max(),
                    "block_section_length": data["block_section_length"].sum(),
                }
            )
        )
        grouped_df.reset_index(inplace=True)
        all_df = grouped_df.groupby("run_id").apply(
            lambda data: pd.Series(
                {
                    "train_type": "all",
                    "enter_tick": 0,
                    "leave_tick": data["leave_tick"].max(),
                    "block_section_length": data["block_section_length"].sum(),
                }
            )
        )
        all_df.reset_index(inplace=True)
        grouped_df = pd.concat([grouped_df, all_df], axis=0)


        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"] * 3600 / row["leave_tick"],
            axis=1,
        )
        grouped_df = grouped_df.groupby(["train_type"]).agg(
            {"verkehrsleistung": "mean"}
        )
        grouped_df.reset_index(inplace=True)
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
            departures_arrivals_df["train_type"] = departures_arrivals_df["train_id"].apply(
                lambda train_id: train_id.split("_")[2]
            )
            departures_arrivals_df["run_id"] = run_id.id
            departures_arrivals_df["config_id"] = run_id.simulation_configuration.id
            df_list.append(departures_arrivals_df)
        departures_arrivals_df = pd.concat(df_list, axis=0)
        out_df = departures_arrivals_df[
            ["config_id", "station_id", "train_id", "train_type", "arrival_tick", "departure_tick"]
        ]
        all_df = out_df.groupby(["config_id", "station_id", "train_id"]).apply(
            lambda data: pd.Series(
                {
                    "train_type": "all",
                    "arrival_tick": self._get_window_size_from_values_threshold(data["arrival_tick"], threshold),
                    "departure_tick": self._get_window_size_from_values_threshold(data["departure_tick"], threshold),
                }
            )
        )
        all_df.reset_index(inplace=True)
        del all_df["station_id"]
        del all_df["train_id"]
        all_df = all_df.groupby(["config_id", "train_type"]).apply(
            lambda data: pd.Series(
                {
                    "arrival_tick": data["arrival_tick"].mean(),
                    "departure_tick": data["departure_tick"].mean(),
                }
            )
        )
        out_df = out_df.groupby(["config_id", "station_id", "train_id", "train_type"]).agg(
            lambda x: self._get_window_size_from_values_threshold(x, threshold)
        )
        out_df.reset_index(inplace=True)
        del out_df["station_id"]
        del out_df["train_id"]
        out_df = out_df.groupby(["config_id", "train_type"]).apply(
            lambda data: pd.Series(
                {
                    "arrival_tick": data["arrival_tick"].mean(),
                    "departure_tick": data["departure_tick"].mean(),
                }
            )
        )
        out_df = pd.concat([out_df, all_df], axis=0)

        out_df.sort_values(by=["config_id", "train_type"], inplace=True)
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
            block_section_times_df["train_type"] = block_section_times_df["train_id"].apply(
                lambda train_id: train_id.split("_")[2]
            )
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby(["config_id", "run_id", "train_type"]).apply(
            lambda data: pd.Series(
                {
                    "enter_tick": 0,
                    "leave_tick": data["leave_tick"].max(),
                    "block_section_length": data["block_section_length"].sum(),
                }
            )
        )

        grouped_df = grouped_df.groupby(["config_id", "train_type"]).agg(
            {"block_section_length": "mean"}
        )
        grouped_df.reset_index(inplace=True)
        all_df = grouped_df.groupby(["config_id"]).apply(
            lambda data: pd.Series(
                {
                    "train_type": "all",
                    "block_section_length": data["block_section_length"].sum(),
                }
            )
        )
        all_df.reset_index(inplace=True)
        grouped_df = pd.concat([grouped_df, all_df], axis=0)
        grouped_df.sort_values(by=["config_id", "train_type"], inplace=True)
        grouped_df.reset_index(inplace=True)
        del grouped_df["index"]
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
            block_section_times_df["train_type"] = block_section_times_df["train_id"].apply(
                lambda train_id: train_id.split("_")[2]
            )
            block_section_times_df["run_id"] = run_id.id
            block_section_times_df["config_id"] = run_id.simulation_configuration.id
            df_list.append(block_section_times_df)
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.dropna(inplace=True)
        block_section_times_df["time"] = block_section_times_df.apply(
            lambda row: row["leave_tick"] - row["enter_tick"], axis=1
        )
        grouped_df = block_section_times_df.groupby(["config_id", "run_id", "train_type"]).apply(
            lambda data: pd.Series(
                {
                    "enter_tick": 0,
                    "leave_tick": data["leave_tick"].max(),
                    "block_section_length": data["block_section_length"].sum(),
                }
            )
        )
        grouped_df.reset_index(inplace=True)
        all_df = grouped_df.groupby(["config_id", "run_id"]).apply(
            lambda data: pd.Series(
                {
                    "train_type": "all",
                    "enter_tick": 0,
                    "leave_tick": data["leave_tick"].max(),
                    "block_section_length": data["block_section_length"].sum(),
                }
            )
        )
        all_df.reset_index(inplace=True)
        grouped_df = pd.concat([grouped_df, all_df], axis=0)

        grouped_df["verkehrsleistung"] = grouped_df.apply(
            lambda row: row["block_section_length"] * 3600 / row["leave_tick"],
            axis=1,
        )
        grouped_df = grouped_df.groupby(["config_id", "train_type"]).agg(
            {"verkehrsleistung": "mean"}
        )
        grouped_df.reset_index(inplace=True)
        grouped_df.sort_values(by=["config_id", "train_type"], inplace=True)
        return grouped_df
