from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfig
from src.interfaces import *


class TrainCancelledFault(Fault):
    """A fault that blocks a platform"""

    affected_element_ID: int = None

    def inject_fault(self, spawn_restrictor: ISpawnerRestrictor):
        """inject TrainCancelledFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train by id
        # - mark train as cancelled
        spawn_restrictor.block_schedule(self.affected_element_ID)

    def resolve_fault(self, spawn_restrictor: ISpawnerRestrictor):
        """resolves the previously injected TrainCancelledFault

        :param component: the component with the injected fault
        :type component: Component
        """
        spawn_restrictor.unblock_schedule(self.affected_element_ID)
