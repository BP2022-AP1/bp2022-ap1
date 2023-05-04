from abc import ABC, abstractmethod

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.fault_injector.fault_strategies import (
    FaultStrategy,
    RandomFaultStrategy,
    RegularFaultStrategy,
)
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Track, Train


class Fault(ABC):
    """An abstract fault for the fault injection"""

    injected: bool = False
    configuration: FaultConfiguration
    logger: Logger
    simulation_object_updater: SimulationObjectUpdatingComponent
    interlocking: IInterlockingDisruptor
    strategy: FaultStrategy

    STRATEGY_CLASSES: dict[str, type] = {
        "regular": RegularFaultStrategy,
        "random": RandomFaultStrategy,
    }

    def __init__(
        self,
        configuration,
        logger: Logger,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        self.configuration = configuration
        self.strategy = self.create_strategy_from_configuration(configuration)
        self.logger = logger
        self.simulation_object_updater = simulation_object_updater
        self.interlocking = interlocking

    def create_strategy_from_configuration(
        self, configuration: FaultConfiguration
    ) -> FaultStrategy:
        """Returns a random or regular strategy, depending on the configuration

        :param configuration: the configuration of the Fault
        :type configuration: FaultConfiguration
        :return: the FaultStrategy for this fault
        :rtype: FaultStrategy
        """
        return self.STRATEGY_CLASSES[configuration.strategy]()

    @abstractmethod
    def inject_fault(self, tick: int):
        """injects the fault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """

        raise NotImplementedError()

    @abstractmethod
    def resolve_fault(self, tick: int):
        """resolves the previously injected fault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """

        raise NotImplementedError()

    def next_tick(self, tick: int):
        """handle the next tick event accordingly

        :param tick: the current simulation tick
        :type tick: int
        """
        if self.strategy.should_inject(tick, self.configuration, self.injected):
            self.inject_fault(tick)
            self.injected = True
        elif self.strategy.should_resolve(tick, self.configuration, self.injected):
            self.resolve_fault(tick)
            self.injected = False


class TrainMixIn:
    """adds the functionality to get the train in which the fault should be injected"""

    def get_train(
        self,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        affected_element_id: str,
    ) -> Train:
        """returns the train in which the requested fault

        :param simulation_object_updater: wrapper component
        :type simulation_object_updater: SimulationObjectUpdatingComponent
        :param affected_element_id: id of the train in which the fault should be injected into
        :type affected_element_id: str
        :return: the train with the requested id
        :rtype: Train
        """
        trains: list[Train] = [
            train
            for train in simulation_object_updater.trains
            if train.identifier == affected_element_id
        ]
        if len(trains) < 1:
            raise ValueError(f"Train {affected_element_id} does not exist")
        return trains[0]

    def get_train_or_none(
        self,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        affected_element_id: str,
    ):
        """Returns the requested train or None, if the train is not in the simulation

        :param simulation_object_updater: wrapper component
        :type simulation_object_updater: SimulationObjectUpdatingComponent
        :param affected_element_id: id of the train in which the fault should be injected into
        :type affected_element_id: str
        :return: the train or None
        :rtype: Train or None
        """
        simulation_train: Train
        try:
            simulation_train = self.get_train(
                simulation_object_updater, affected_element_id
            )
        except ValueError:
            simulation_train = None
        return simulation_train


class TrackMixIn:
    """adds the functionality to get the track in which the fault should be injected"""

    def get_track(
        self,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        affected_element_id: str,
    ) -> Track:
        """returns the track in which the requested fault

        :param simulation_object_updater: wrapper component
        :type simulation_object_updater: SimulationObjectUpdatingComponent
        :param affected_element_id: id of the track in which the fault should be injected into
        :type affected_element_id: str
        :return: the track with the requested id
        :rtype: Track
        """
        tracks: list[Track] = [
            track
            for track in simulation_object_updater.tracks
            if track.identifier == affected_element_id
        ]
        if len(tracks) < 1:
            raise ValueError(f"Track {affected_element_id} does not exist")
        return tracks[0]
