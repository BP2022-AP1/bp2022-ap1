from uuid import UUID

import pandas as pd

from src.logger.log_entry import (
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainEnterBlockSectionLogEntry,
    TrainLeaveBlockSectionLogEntry,
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

    def _get_departures_of_train(self, run_id: UUID, train_id: str) -> pd.DataFrame:
        """Returns a DataFrame containing all departures of the given train in
        the given run.
        :param run_id: The id of the run.
        :param train_id: The id of the train.
        :return: A DataFrame containing all departures of the given train in
        the given run."""

        departures = TrainDepartureLogEntry.select().where(
            TrainDepartureLogEntry.run_id == run_id
            and TrainDepartureLogEntry.train_id == train_id
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
            TrainArrivalLogEntry.run_id == run_id
            and TrainArrivalLogEntry.train_id == train_id
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
        departures_arrivals_df = pd.concat(df_list, axis=0)
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
                    TrainEnterBlockSectionLogEntry.run_id == run_id
                    and TrainEnterBlockSectionLogEntry.train_id == train_id
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
                    TrainLeaveBlockSectionLogEntry.run_id == run_id
                    and TrainLeaveBlockSectionLogEntry.train_id == train_id
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
