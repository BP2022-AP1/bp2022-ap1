from uuid import UUID

import numpy as np
import pandas as pd

from src.implementor.models import SimulationConfiguration, Run
from src.logger.log_entry import (
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainEnterBlockSectionLogEntry,
    TrainLeaveBlockSectionLogEntry, InjectFaultLogEntry, ResolveFaultLogEntry,
)


class LogCollector:
    """The LogCollector is responsible for collecting all logs of a run and
    providing them in a structured way."""

    def _get_trains_departure_arrivals(self, run_id: UUID) -> list[str]:
        """Returns a list of all trains that have departed or arrived in the
        given run.
        :param run_id: The id of the run.
        :return: A list of all trains that have departed or arrived in the
        given run.
        """

        trains_arrivals = (
            TrainArrivalLogEntry.select(TrainArrivalLogEntry.train_id)
            .distinct()
            .where(TrainArrivalLogEntry.run_id == run_id)
        )
        trains_departures = (
            TrainDepartureLogEntry.select(TrainDepartureLogEntry.train_id)
            .distinct()
            .where(TrainDepartureLogEntry.run_id == run_id)
        )
        train_ids = {t.train_id for t in trains_arrivals}
        train_ids = train_ids.union({t.train_id for t in trains_departures})
        return list(train_ids)

    def get_trains(self) -> list[str]:
        """Returns a list of all trains.
        :return: A list of all trains.
        """

        trains_arrivals = (
            TrainArrivalLogEntry.select(TrainArrivalLogEntry.train_id)
            .distinct()
        )
        trains_departures = (
            TrainDepartureLogEntry.select(TrainDepartureLogEntry.train_id)
        )
        trains_enter = (
            TrainEnterBlockSectionLogEntry.select(
                TrainEnterBlockSectionLogEntry.train_id
            )
            .distinct()
        )
        trains_leave = (
            TrainLeaveBlockSectionLogEntry.select(
                TrainLeaveBlockSectionLogEntry.train_id
            )
            .distinct()
        )

        trains = {t.train_id for t in trains_arrivals}
        trains = trains.union({t.train_id for t in trains_departures})
        trains = trains.union({t.train_id for t in trains_enter})
        trains = trains.union({t.train_id for t in trains_leave})
        return list(trains)

    def get_stations(self) -> list[str]:
        """Returns a list of all stations.
        :return: A list of all stations.
        """

        stations_arrivals = (
            TrainArrivalLogEntry.select(TrainArrivalLogEntry.station_id)
            .distinct()
        )
        stations_departures = (
            TrainDepartureLogEntry.select(TrainDepartureLogEntry.station_id)
            .distinct()
        )
        station_ids = {t.station_id for t in stations_arrivals}
        station_ids = station_ids.union({t.station_id for t in stations_departures})
        return list(station_ids)

    def get_run_ids(self) -> list[UUID]:
        """Returns a list of all run ids.
        :return: A list of all run ids.
        """
        run_ids = [r.id for r in Run.select(Run.id).distinct()]
        return list(run_ids)

    def get_config_ids(self) -> list[UUID]:
        """Returns a list of all config ids.
        :return: A list of all config ids.
        """

        config_ids = [c.id for c in SimulationConfiguration.select(SimulationConfiguration.id).distinct()]
        return list(config_ids)

    def _get_departures_of_train(self, run_id: UUID, train_id: str) -> pd.DataFrame:
        """Returns a DataFrame containing all departures of the given train in
        the given run.
        :param run_id: The id of the run.
        :param train_id: The id of the train.
        :return: A DataFrame containing all departures of the given train in
        the given run."""

        departures = TrainDepartureLogEntry.select().where(
            (TrainDepartureLogEntry.run_id == run_id)
            & (TrainDepartureLogEntry.train_id == train_id)
        )
        # pylint will not recognize that peewee results are iterable
        # pylint: disable=not-an-iterable
        departures_df = pd.DataFrame(
            [[d.tick, d.station_id] for d in departures], columns=["tick", "station_id"]
        )
        departures_df = departures_df.sort_values("tick")
        return departures_df

    def _get_arrivals_of_train(self, run_id: UUID, train_id: str) -> pd.DataFrame:
        """Returns a DataFrame containing all arrivals of the given train in
        the given run.
        :param run_id: The id of the run.
        :param train_id: The id of the train.
        :return: A DataFrame containing all arrivals of the given train in
        the given run."""

        arrivals = TrainArrivalLogEntry.select().where(
            (TrainArrivalLogEntry.run_id == run_id)
            & (TrainArrivalLogEntry.train_id == train_id)
        )
        # pylint will not recognize that peewee results are iterable
        # pylint: disable=not-an-iterable
        arrivals_df = pd.DataFrame(
            [[a.tick, a.station_id] for a in arrivals], columns=["tick", "station_id"]
        )
        arrivals_df = arrivals_df.sort_values("tick")
        return arrivals_df

    def get_departures_arrivals_of_train(
            self, run_id: UUID, train_id: str
    ) -> pd.DataFrame:
        """Returns a DataFrame containing all departures and arrivals of the
        given train in the given run.
        :param run_id: The id of the run.
        :param train_id: The id of the train.
        :return: A DataFrame containing all departures and arrivals of the
        given train in the given run."""

        arrivals = self._get_arrivals_of_train(run_id, train_id)
        departures = self._get_departures_of_train(run_id, train_id)

        arrivals_first = arrivals.iloc[0].tick < departures.iloc[0].tick
        arrivals_last = arrivals.iloc[-1].tick > departures.iloc[-1].tick
        station_list = arrivals.station_id
        arrivals_list = arrivals.tick
        departures_list = departures.tick
        if not arrivals_first:
            arrivals_list = [None] + list(arrivals_list)
            station_list = [departures.iloc[0].station_id] + list(station_list)
        if arrivals_last:
            departures_list = list(departures_list) + [None]
        departures_arrivals_df = pd.DataFrame(
            zip(station_list, arrivals_list, departures_list),
            columns=["station_id", "arrival_tick", "departure_tick"],
        )
        departures_arrivals_df = departures_arrivals_df.replace(np.nan, None)
        departures_arrivals_df['arrival_tick'] = departures_arrivals_df['arrival_tick'].astype('Int64')
        departures_arrivals_df['departure_tick'] = departures_arrivals_df['departure_tick'].astype('Int64')
        return departures_arrivals_df

    def get_departures_arrivals_all_trains(self, run_id: UUID) -> pd.DataFrame:
        """Returns a DataFrame containing all departures and arrivals of all
        trains in the given run.
        :param run_id: The id of the run.
        :return: A DataFrame containing all departures and arrivals of all
        trains in the given run."""

        df_list = []
        for train_id in self._get_trains_departure_arrivals(run_id):
            departures_arrivals_df = self.get_departures_arrivals_of_train(
                run_id, train_id
            )
            departures_arrivals_df["train_id"] = train_id
            df_list += [departures_arrivals_df]
        if len(df_list) == 0:
            return pd.DataFrame(columns=["train_id", "station_id", "arrival_tick", "departure_tick"])
        if len(df_list) > 1:
            departures_arrivals_df = pd.concat(df_list, axis=0)
        else:
            departures_arrivals_df = df_list[0]
        departures_arrivals_df.sort_values(["train_id", "departure_tick"], inplace=True)
        departures_arrivals_df = departures_arrivals_df.reset_index(drop=True)
        return departures_arrivals_df

    def _get_trains_block_section(self, run_id: UUID) -> list[str]:
        """Returns a list of all trains that have entered or left a block
        section in the given run.
        :param run_id: The id of the run.
        :return: A list of all trains that have entered or left a block"""

        trains_enter = (
            TrainEnterBlockSectionLogEntry.select(
                TrainEnterBlockSectionLogEntry.train_id
            )
            .distinct()
            .where(TrainEnterBlockSectionLogEntry.run_id == run_id)
        )
        trains_leave = (
            TrainLeaveBlockSectionLogEntry.select(
                TrainLeaveBlockSectionLogEntry.train_id
            )
            .distinct()
            .where(TrainLeaveBlockSectionLogEntry.run_id == run_id)
        )
        train_ids = {t.train_id for t in trains_enter}
        train_ids = train_ids.union({t.train_id for t in trains_leave})
        return list(train_ids)

    def get_block_section_times_of_train(
            self, run_id: UUID, train_id: str
    ) -> pd.DataFrame:
        """Returns a DataFrame containing all block section times of the
        given train in the given run.
        :param run_id: The id of the run.
        :param train_id: The id of the train.
        :return: A DataFrame containing all block section times of the
        given train in the given run."""

        # pylint will not recognize that peewee results are iterable
        # pylint: disable=not-an-iterable
        train_enter_df = pd.DataFrame(
            [
                [e.tick, e.block_section_id, e.block_section_length]
                for e in TrainEnterBlockSectionLogEntry.select().where(
                (TrainEnterBlockSectionLogEntry.run_id == run_id)
                & (TrainEnterBlockSectionLogEntry.train_id == train_id)
            )
            ],
            columns=["tick", "block_section_id", "block_section_length"],
        )
        # pylint will not recognize that peewee results are iterable
        # pylint: disable=not-an-iterable
        train_leave_df = pd.DataFrame(
            [
                [e.tick, e.block_section_id, e.block_section_length]
                for e in TrainLeaveBlockSectionLogEntry.select().where(
                (TrainLeaveBlockSectionLogEntry.run_id == run_id)
                & (TrainLeaveBlockSectionLogEntry.train_id == train_id)
            )
            ],
            columns=["tick", "block_section_id", "block_section_length"],
        )
        train_enter_df = train_enter_df.sort_values("tick")
        train_leave_df = train_leave_df.sort_values("tick")

        train_enter_first = train_enter_df.iloc[0].tick < train_leave_df.iloc[0].tick
        train_enter_last = train_enter_df.iloc[-1].tick >= train_leave_df.iloc[-1].tick
        block_section_ids = train_enter_df.block_section_id
        block_lengths = train_enter_df.block_section_length
        enter_ticks = train_enter_df.tick
        leave_ticks = train_leave_df.tick
        if not train_enter_first:
            enter_ticks = [None] + list(enter_ticks)
            block_section_ids = [train_leave_df.iloc[0].block_section_id] + list(
                block_section_ids
            )
            block_lengths = [train_leave_df.iloc[0].block_section_length] + list(
                block_lengths
            )
        if train_enter_last:
            leave_ticks = list(leave_ticks) + [None]
        block_section_times_df = pd.DataFrame(
            zip(enter_ticks, leave_ticks, block_section_ids, block_lengths),
            columns=[
                "enter_tick",
                "leave_tick",
                "block_section_id",
                "block_section_length",
            ],
        )
        return block_section_times_df

    def get_block_section_times_all_trains(self, run_id: UUID) -> pd.DataFrame:
        """Returns a DataFrame containing all block section times of all
        trains in the given run.
        :param run_id: The id of the run.
        :return: A DataFrame containing all block section times of all
        trains in the given run."""

        df_list = []
        for train_id in self._get_trains_block_section(run_id):
            block_section_times_df = self.get_block_section_times_of_train(
                run_id, train_id
            )
            block_section_times_df["train_id"] = train_id
            df_list += [block_section_times_df]
        block_section_times_df = pd.concat(df_list, axis=0)
        block_section_times_df.sort_values(["train_id", "leave_tick"], inplace=True)
        block_section_times_df = block_section_times_df.reset_index(drop=True)
        return block_section_times_df

    def _parse_inject_log_entry(self, entry: InjectFaultLogEntry) -> tuple:
        """Parses a log entry of a fault injection.
        :param entry: The log entry.
        :return: A dictionary containing the parsed log entry."""
        tick = entry.tick
        affected_element = entry.affected_element
        value_before = entry.value_before
        value_after = entry.value_after
        fault_type = None
        fault_id = None
        if entry.platform_blocked_fault_configuration is not None:
            fault_type = "platform_blocked"
            fault_id = entry.platform_blocked_fault_configuration
        elif entry.track_blocked_fault_configuration is not None:
            fault_type = "track_blocked"
            fault_id = entry.track_blocked_fault_configuration
        elif entry.track_speed_limit_fault_configuration is not None:
            fault_type = "track_speed_limit"
            fault_id = entry.track_speed_limit_fault_configuration
        elif entry.schedule_blocked_fault_configuration is not None:
            fault_type = "schedule_blocked"
            fault_id = entry.schedule_blocked_fault_configuration
        elif entry.train_prio_fault_configuration is not None:
            fault_type = "train_prio"
            fault_id = entry.train_prio_fault_configuration
        elif entry.train_speed_fault_configuration is not None:
            fault_type = "train_speed"
            fault_id = entry.train_speed_fault_configuration

        return tick, fault_type, fault_id, affected_element, value_before, value_after

    def _parse_resolve_log_entry(self, entry: ResolveFaultLogEntry) -> tuple:
        """Parses a log entry of a fault resolution.
        :param entry: The log entry.
        :return: A dictionary containing the parsed log entry."""
        tick = entry.tick
        fault_type = None
        fault_id = None
        if entry.platform_blocked_fault_configuration is not None:
            fault_type = "platform_blocked"
            fault_id = entry.platform_blocked_fault_configuration
        elif entry.track_blocked_fault_configuration is not None:
            fault_type = "track_blocked"
            fault_id = entry.track_blocked_fault_configuration
        elif entry.track_speed_limit_fault_configuration is not None:
            fault_type = "track_speed_limit"
            fault_id = entry.track_speed_limit_fault_configuration
        elif entry.schedule_blocked_fault_configuration is not None:
            fault_type = "schedule_blocked"
            fault_id = entry.schedule_blocked_fault_configuration
        elif entry.train_prio_fault_configuration is not None:
            fault_type = "train_prio"
            fault_id = entry.train_prio_fault_configuration
        elif entry.train_speed_fault_configuration is not None:
            fault_type = "train_speed"
            fault_id = entry.train_speed_fault_configuration

        return tick, fault_type, fault_id

    def get_faults(self, run_id: UUID) -> pd.DataFrame:
        """Returns a DataFrame containing all faults in the given run.
        :param run_id: The id of the run.
        :return: A DataFrame containing all faults in the given run."""
        fault_df = pd.DataFrame([self._parse_inject_log_entry(fault) for fault in
                                 InjectFaultLogEntry.select().where(InjectFaultLogEntry.run_id == run_id)],
                                columns=["begin_tick", "fault_type", "fault_id", "affected_element",
                                         "value_before", "value_after"])

        resolve_df = pd.DataFrame([self._parse_resolve_log_entry(fault) for fault in
                                   ResolveFaultLogEntry.select().where(ResolveFaultLogEntry.run_id == run_id)],
                                  columns=["end_tick", "fault_type", "fault_id"])
        faults_df = pd.merge(fault_df, resolve_df, on=["fault_type", "fault_id"], how="outer")
        faults_df["fault_id"] = faults_df["fault_id"].astype('string')
        return faults_df
