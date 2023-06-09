from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault, TrainMixIn
from src.wrapper.simulation_objects import Train


class TrainPrioFault(Fault, TrainMixIn):
    """A fault affecting the priority of trains."""

    configuration: TrainPrioFaultConfiguration
    old_prio: int
    train: Train = None

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

        self.interlocking_disruptor.insert_train_priority_changed(self.train)
        self.event_bus.inject_train_prio_fault(
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
        if self.train is None:
            raise ValueError("TrainPrioFault not injected")

        if self.train is self.get_train_or_none(
            self.simulation_object_updater, self.train.identifier
        ):
            self.train.train_type.priority = self.old_prio
            self.interlocking_disruptor.insert_train_priority_changed(self.train)
        self.event_bus.resolve_train_prio_fault(tick, self.configuration.id)
