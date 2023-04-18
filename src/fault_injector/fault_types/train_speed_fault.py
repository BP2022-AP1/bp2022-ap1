from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Train


class TrainSpeedFault(Fault):
    """A fault affecting the speed of trains."""

    configuration: TrainSpeedFaultConfiguration
    train: Train
    wrapper: SimulationObjectUpdatingComponent
    interlocking: IInterlockingDisruptor

    # pylint: disable=duplicate-code
    # Otherwise another inheritance layer would be needed.
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
    # pylint: enable=duplicate-code

    def inject_fault(self, tick: int):
        """inject TrainSpeedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        # - get train object
        # - save the current speed of the train in old_speed
        # - set train speed to new_speed
        raise NotImplementedError()

    def resolve_fault(self, tick: int):
        """resolves the previously injected TrainSpeedFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        # - get train object
        # - set the train speed to old_speed

        raise NotImplementedError()
