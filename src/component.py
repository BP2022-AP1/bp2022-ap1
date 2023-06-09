from abc import ABC, abstractmethod

from src.event_bus.event_bus import EventBus


class Component(ABC):
    """Interface for components that receive ticks."""

    event_bus: EventBus
    priority: int

    PRIORITY_LEVELS: dict[str, int] = {"VERY_HIGH": 10, "HIGH": 9, "MEDIUM": 8, "LOW": 7}

    def __init__(self, event_bus: EventBus, priority: str):
        """Initializes the component.

        :param event_bus: reference to the global event_bus
        :param priority: priority of the component for sorting purposes
        """
        self.event_bus = event_bus
        self.priority = self.PRIORITY_LEVELS[priority]

    @abstractmethod
    def next_tick(self, tick: int):
        """
        Called to announce that the next tick occurred.
        :param tick: The current tick.
        :rtype: None
        """
        raise NotImplementedError()


class MockComponent(Component):
    """Mock for a simple component to check if next tick is called"""

    def __init__(self):
        Component.__init__(self, None, 1)

    def next_tick(self, tick: int):
        pass
