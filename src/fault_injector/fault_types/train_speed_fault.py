from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault, TrainMixIn
from src.wrapper.simulation_objects import Train


class TrainSpeedFault(Fault, TrainMixIn):
    """A fault affecting the speed of trains."""

    configuration: TrainSpeedFaultConfiguration
    old_speed: float
    train: Train = None

    def inject_fault(self, tick: int):
        """inject TrainSpeedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.train: Train = self.get_train(
            self.simulation_object_updater, self.configuration.affected_element_id
        )

        self.old_speed = self.train.train_type.max_speed
        self.train.train_type.max_speed = self.configuration.new_speed

        # The following is currently not implemented, comment in later
        # self.interlocking_disruptor.insert_train_max_speed_changed(self.train)
        self.event_bus.inject_train_speed_fault(
            tick,
            self.configuration.id,
            self.train.identifier,
            self.old_speed,
            self.configuration.new_speed,
        )

    def resolve_fault(self, tick: int):
        """resolves the previously injected TrainSpeedFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        if self.train is None:
            raise ValueError("TrainSpeedFault not injected")

        if self.train is self.get_train_or_none(
            self.simulation_object_updater, self.train.identifier
        ):
            self.train.train_type.max_speed = self.old_speed
            # The following is currently not implemented, comment in later
            # self.interlocking_disruptor.insert_train_max_speed_changed(self.train)
        self.event_bus.resolve_train_speed_fault(tick, self.configuration.id)
