from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.logger.logger import Logger
from src.spawner.spawner import Spawner


class ScheduleBlockedFault(Fault):
    """A fault that blocks a platform"""

    configuration: ScheduleBlockedFaultConfiguration
    spawner: Spawner

    def __init__(
        self,
        configuration,
        logger: Logger,
        spawner: Spawner,
    ):
        super().__init__(configuration, logger)
        self.spawner = spawner

    def inject_fault(self, tick: int):
        """inject ScheduleBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.spawner.block_schedule(self.configuration.affected_element_id)
        self.logger.inject_schedule_blocked_fault(
            tick=tick,
            schedule_blocked_fault_configuration=self.configuration.id,
            affected_element=self.configuration.affected_element_id,
        )
        # - get schedule by id
        # - mark schedule as blocked

    def resolve_fault(self, tick: int):
        """resolves the previously injected ScheduleBlockedFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        self.spawner.unblock_schedule(self.configuration.affected_element_id)
        self.logger.resolve_schedule_blocked_fault(
            tick=tick, schedule_blocked_fault_configuration=self.configuration.id
        )
