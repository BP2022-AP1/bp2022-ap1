from abc import ABC, abstractmethod

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Track, Train


class Fault(ABC):
    """An abstract fault for the fault injection"""

    configuration: FaultConfiguration
    logger: Logger
    wrapper: SimulationObjectUpdatingComponent
    interlocking: IInterlockingDisruptor

    def __init__(
        self,
        configuration,
        logger: Logger,
        wrapper: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        self.configuration = configuration
        self.logger = logger
        self.wrapper = wrapper
        self.interlocking = interlocking

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
        if tick == self.configuration.start_tick:
            self.inject_fault(tick=tick)
        elif tick == self.configuration.end_tick:
            self.resolve_fault(tick=tick)


class TrainMixIn:
    """adds the functionality to get the train in which the fault should be injected"""

    def get_train(
        self, wrapper: SimulationObjectUpdatingComponent, affected_element_id: str
    ) -> Train:
        """returns the train in which the requested fault

        :param wrapper: wrapper component
        :type wrapper: SimulationObjectUpdatingComponent
        :param affected_element_id: id of the train in which the fault should be injected into
        :type affected_element_id: str
        :return: the train with the requested id
        :rtype: Train
        """
        return [
            train for train in wrapper.trains if train.identifier == affected_element_id
        ][0]


class TrackMixIn:
    """adds the functionality to get the track in which the fault should be injected"""

    def get_track(
        self, wrapper: SimulationObjectUpdatingComponent, affected_element_id: str
    ) -> Track:
        """returns the track in which the requested fault

        :param wrapper: wrapper component
        :type wrapper: SimulationObjectUpdatingComponent
        :param affected_element_id: id of the track in which the fault should be injected into
        :type affected_element_id: str
        :return: the track with the requested id
        :rtype: Track
        """
        return [
            track for track in wrapper.tracks if track.identifier == affected_element_id
        ][0]
