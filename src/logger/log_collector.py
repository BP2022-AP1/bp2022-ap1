from uuid import UUID

from src.implementor.models import Run, SimulationConfiguration, Token
from src.logger.log_entry import TrainDepartureLogEntry, TrainArrivalLogEntry, TrainEnterBlockSectionLogEntry, \
    TrainLeaveBlockSectionLogEntry
from src.logger.logger import Logger

import pandas as pd


class LogCollector:
    def __init__(self):
        pass

    def get_departures_all_trains(self, run_id: UUID):
        departures = (TrainDepartureLogEntry
                      .select()
                      .where(TrainDepartureLogEntry.run_id == run_id)
                      )
        df = pd.DataFrame([[d.train_id, d.tick, d.station_id] for d in departures],
                          columns=['train_id', 'tick', 'station_id'])
        df = df.sort_values('tick')
        return df

    def get_arrivals_all_trains(self, run_id: UUID):
        arrivals = (TrainArrivalLogEntry
                    .select()
                    .where(TrainArrivalLogEntry.run_id == run_id)
                    )
        df = pd.DataFrame([[a.train_id, a.tick, a.station_id] for a in arrivals],
                          columns=['train_id', 'tick', 'station_id'])
        df = df.sort_values('tick')
        return df

    def get_trains_departure_arrivals(self, run_id: UUID):
        trains_arrivals = (TrainArrivalLogEntry
                           .select(TrainArrivalLogEntry.train_id)
                           .distinct()
                           .where(TrainArrivalLogEntry.run_id == run_id)
                           )
        trains_departures = (TrainDepartureLogEntry
                             .select(TrainDepartureLogEntry.train_id)
                             .distinct()
                             .where(TrainDepartureLogEntry.run_id == run_id)
                             )
        train_ids = set([t.train_id for t in trains_arrivals])
        train_ids = train_ids.union(set([t.train_id for t in trains_departures]))
        return list(train_ids)

    def get_departures_arrivals_all_trains(self, run_id: UUID):
        df_list = []
        for train_id in self.get_trains_departure_arrivals(run_id):
            df = self.get_departures_arrivals_of_train(run_id, train_id)
            df['train_id'] = train_id
            df_list += [df]

        return pd.concat(df_list, axis=0)

    def get_departures_of_train(self, run_id: UUID, train_id: str):
        departures = (
            TrainDepartureLogEntry
            .select()
            .where(
                TrainDepartureLogEntry.run_id == run_id
                and TrainDepartureLogEntry.train_id == train_id
            ))
        df = pd.DataFrame([[d.tick, d.station_id] for d in departures], columns=['tick', 'station_id'])
        df = df.sort_values('tick')
        return df

    def get_arrivals_of_train(self, run_id: UUID, train_id: str):
        arrivals = (
            TrainArrivalLogEntry
            .select()
            .where(
                TrainArrivalLogEntry.run_id == run_id
                and TrainArrivalLogEntry.train_id == train_id
            ))
        df = pd.DataFrame([[a.tick, a.station_id] for a in arrivals], columns=['tick', 'station_id'])
        df = df.sort_values('tick')
        return df

    def get_departures_arrivals_of_train(self, run_id: UUID, train_id: str):
        # TODO test for 4 cases of Verschiebung
        # TODO dypes change to int
        arrivals = self.get_arrivals_of_train(run_id, train_id)
        departures = self.get_departures_of_train(run_id, train_id)

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
        df = pd.DataFrame(zip(station_list, arrivals_list, departures_list),
                          columns=['station_id', 'arrival_tick', 'departure_tick'])
        return df

    def get_trains_block_section(self, run_id: UUID):
        trains_enter = (TrainEnterBlockSectionLogEntry
                        .select(TrainEnterBlockSectionLogEntry.train_id)
                        .distinct()
                        .where(TrainEnterBlockSectionLogEntry.run_id == run_id)
                        )
        trains_leave = (TrainLeaveBlockSectionLogEntry
                        .select(TrainLeaveBlockSectionLogEntry.train_id)
                        .distinct()
                        .where(TrainLeaveBlockSectionLogEntry.run_id == run_id)
                        )
        train_ids = set([t.train_id for t in trains_enter])
        train_ids = train_ids.union(set([t.train_id for t in trains_leave]))
        return list(train_ids)

    def get_block_section_times(self, run_id: UUID):
        df_list = []
        for train_id in self.get_trains_block_section(run_id):
            df = self.get_block_section_times_of_train(run_id, train_id)
            df['train_id'] = train_id
            df_list += [df]

        return pd.concat(df_list, axis=0)

    def get_block_section_times_of_train(self, run_id: UUID, train_id: str):
        train_enter_df = pd.DataFrame(
            [[e.tick, e.block_section_id, e.block_section_length] for e in TrainEnterBlockSectionLogEntry
            .select()
            .where(
                TrainEnterBlockSectionLogEntry.run_id == run_id
                and TrainEnterBlockSectionLogEntry.train_id == train_id
            )
             ], columns=['tick', 'block_section_id', 'block_section_length'])
        train_leave_df = pd.DataFrame(
            [[e.tick, e.block_section_id, e.block_section_length] for e in TrainLeaveBlockSectionLogEntry
            .select()
            .where(
                TrainLeaveBlockSectionLogEntry.run_id == run_id
                and TrainLeaveBlockSectionLogEntry.train_id == train_id
            )
             ], columns=['tick', 'block_section_id', 'block_section_length']
        )
        train_enter_df = train_enter_df.sort_values('tick')
        train_leave_df = train_leave_df.sort_values('tick')

        train_enter_first = train_enter_df.iloc[0].tick < train_leave_df.iloc[0].tick
        train_enter_last = train_enter_df.iloc[-1].tick >= train_leave_df.iloc[-1].tick
        block_section_ids = train_enter_df.block_section_id
        block_lengths = train_enter_df.block_section_length
        enter_ticks = train_enter_df.tick
        leave_ticks = train_leave_df.tick
        if not train_enter_first:
            enter_ticks = [None] + list(enter_ticks)
            block_section_ids = [train_leave_df.iloc[0].block_section_id] + list(block_section_ids)
            block_lengths = [train_leave_df.iloc[0].block_section_length] + list(block_lengths)
        if train_enter_last:
            leave_ticks = list(leave_ticks) + [None]
        df = pd.DataFrame(zip(enter_ticks, leave_ticks, block_section_ids, block_lengths),
                          columns=['enter_tick', 'leave_tick', 'block_section_id', 'block_section_length'])
        return df


if __name__ == '__main__':
    token = Token.create(permission='test', name='test name', hashedToken='hash')
    simulation_configuration = SimulationConfiguration.create(token=token.id)
    run = Run.create(simulation_configuration=simulation_configuration)
    print('Runs', [run for run in Run.select()])

    print('Run id', run.id)
    logger = Logger(run.id)
    logger.departure_train(10, 'ice_2', 'hbf')
    logger.departure_train(11, 'ice_3', 'hbf')
    logger.arrival_train(20, 'ice_2', 'nord')
    logger.arrival_train(21, 'ice_3', 'nord')
    logger.departure_train(25, 'ice_2', 'nord')
    logger.departure_train(26, 'ice_3', 'nord')
    logger.arrival_train(40, 'ice_2', 'a')
    logger.departure_train(45, 'ice_2', 'a')
    logger.arrival_train(100, 'ice_2', 'b')
    logger.departure_train(105, 'ice_2', 'b')
    logger.arrival_train(150, 'ice_2', 'c')
    logger.departure_train(155, 'ice_2', 'c')
    logger.arrival_train(170, 'ice_2', 'd')

    log_collector = LogCollector()
    print('Departures of train\n', log_collector.get_departures_of_train(run.id, 'ice_2'))
    print('Arrivals of train\n', log_collector.get_arrivals_of_train(run.id, 'ice_2'))
    print('Departures/arrivals of train\n', log_collector.get_departures_arrivals_of_train(run.id, 'ice_2'))
    print('Departures/arrivals of all\n', log_collector.get_departures_arrivals_all_trains(run.id))

    logger.train_enter_block_section(10, 'ice_2', 'a_', 30.2)
    logger.train_enter_block_section(11, 'ice_3', 'b_', 3.2)
    logger.train_leave_block_section(14, 'ice_3', 'b_', 3.2)
    logger.train_enter_block_section(14, 'ice_3', 'c_', 102.3)
    logger.train_leave_block_section(15, 'ice_2', 'a_', 30.2)
    logger.train_enter_block_section(15, 'ice_2', 'b_', 3.2)
    logger.train_leave_block_section(20, 'ice_2', 'b_', 3.2)

    print('Block section entries\n', log_collector.get_block_section_times_of_train(run.id, 'ice_2'))
    print('All trains block section\n', log_collector.get_block_section_times(run.id))
