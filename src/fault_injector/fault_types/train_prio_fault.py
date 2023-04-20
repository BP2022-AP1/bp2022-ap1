from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Train


class TrainPrioFault(Fault):
    """A fault affecting the priority of trains."""

    configuration: TrainPrioFaultConfiguration
    old_prio: int
    train: Train
    wrapper: SimulationObjectUpdatingComponent
    interlocking: IInterlockingDisruptor

    # pylint: disable=duplicate-code
    # Otherwise another inheritance layer would be needed. This will be refactored in the future
    def __init__(
        self,
        configuration,
        logger: Logger,
        wrapper: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        super().__init__(configuration, logger)
        self.wrapper = wrapper
        self.interlocking = interlocking

    def inject_fault(self, tick: int):
        """inject TrainPrioFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.train: Train = [
            train
            for train in self.wrapper.trains
            if train.identifier == self.configuration.affected_element_id
        ][0]
        # pylint: enable=duplicate-code
        self.old_prio = self.train.train_type.priority
        self.train.train_type.priority = self.configuration.new_prio

        self.interlocking.insert_train_priority_changed(self.train.identifier)
        self.logger.inject_train_prio_fault(
            tick,
            self.configuration.id,
            self.train.identifier,
            self.old_prio,
            self.configuration.new_prio,
        )

    def resolve_fault(self, tick: int):
        """resolves the previously injected TrainPrioFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        self.train.train_type.priority = self.old_prio
        self.interlocking.insert_train_priority_changed(self.train.identifier)
        self.logger.resolve_train_prio_fault(tick, self.configuration.id)
