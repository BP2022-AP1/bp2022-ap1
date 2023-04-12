from src.component import Component
from src.fault_injector.fault_types.fault import Fault


class TrackBlockedFault(Fault):
    """A fault that blocks a track"""

    def inject_fault(self, component: Component):
        """inject TrackBlockedFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get track by id
        # - mark track as blocked
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        """resolves the previously injected fault

        :param component: the component with the injected TrackBlockedFault
        :type component: Component
        """
        # - get track by id
        # - mark track as no longer blocked
        raise NotImplementedError()
