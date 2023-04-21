from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault, TrainMixIn
from src.wrapper.simulation_objects import Train


class TrainPrioFault(Fault, TrainMixIn):
    """A fault affecting the priority of trains."""

    configuration: TrainPrioFaultConfiguration
    old_prio: int
    train: Train

    def inject_fault(self, tick: int):
        """inject TrainPrioFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.train: Train = self.get_train(
            self.simulation_object_updater, self.configuration.affected_element_id
        )

        self.old_prio = self.train.train_type.priority
        self.train.train_type.priority = self.configuration.new_prio

        self.interlocking.insert_train_priority_changed(self.train)
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
        if self.train is None or self.train is not self.get_train(
            self.simulation_object_updater, self.train.identifier
        ):
            raise ValueError("Train does not exist or fault not injected")

        self.train.train_type.priority = self.old_prio
        self.interlocking.insert_train_priority_changed(self.train)
        self.logger.resolve_train_prio_fault(tick, self.configuration.id)
