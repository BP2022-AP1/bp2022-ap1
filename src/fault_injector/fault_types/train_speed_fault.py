from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault, TrainMixIn
from src.wrapper.simulation_objects import Train


class TrainSpeedFault(Fault, TrainMixIn):
    """A fault affecting the speed of trains."""

    configuration: TrainSpeedFaultConfiguration
    old_speed: float
    train: Train

    def inject_fault(self, tick: int):
        """inject TrainSpeedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.train: Train = self.get_train(
            self.wrapper, self.configuration.affected_element_id
        )
        self.old_speed = self.train.train_type.max_speed
        self.train.train_type.max_speed = self.configuration.new_speed

        self.interlocking.insert_train_max_speed_changed(self.train.identifier)
        self.logger.inject_train_speed_fault(
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
        self.train.train_type.max_speed = self.old_speed
        self.interlocking.insert_train_max_speed_changed(self.train.identifier)
        self.logger.resolve_train_speed_fault(tick, self.configuration.id)
