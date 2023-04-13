from src.fault_injector.fault_types.fault import Fault


class TrainSpeedFault(Fault):
    """A fault affecting the speed of trains."""

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
