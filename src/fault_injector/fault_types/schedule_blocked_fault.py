from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
from src.fault_injector.fault_types.fault import Fault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.spawner.spawner import Spawner
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)


class ScheduleBlockedFault(Fault):
    """A fault that blocks a platform"""

    configuration: ScheduleBlockedFaultConfiguration
    spawner: Spawner

    def __init__(
        self,
        configuration,
        event_bus: EventBus,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking_disruptor: IInterlockingDisruptor,
        spawner: Spawner,
    ):
        super().__init__(
            configuration, event_bus, simulation_object_updater, interlocking_disruptor
        )
        self.spawner = spawner

    def inject_fault(self, tick: int):
        """inject ScheduleBlockedFault into the given component

        :param tick: the simulation tick in which inject_fault was called
        :type tick: Integer
        """
        self.spawner.block_schedule(self.configuration.affected_element_id)
        self.event_bus.inject_schedule_blocked_fault(
            tick=tick,
            schedule_blocked_fault_configuration=self.configuration.id,
            affected_element=self.configuration.affected_element_id,
        )

    def resolve_fault(self, tick: int):
        """resolves the previously injected ScheduleBlockedFault

        :param tick: the simulation tick in which resolve_fault was called
        :type tick: Integer
        """
        self.spawner.unblock_schedule(self.configuration.affected_element_id)
        self.event_bus.resolve_schedule_blocked_fault(
            tick=tick, schedule_blocked_fault_configuration=self.configuration.id
        )
