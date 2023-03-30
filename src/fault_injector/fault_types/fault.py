from abc import ABC, abstractmethod

from src.base_model import BaseModel
from src.component import Component
from peewee import *


class Fault(ABC):
    """An abstract fault for the fault injection"""

    @abstractmethod
    def inject_fault(self, component: Component):
        """injects the fault into the given component

        :param component: the component the fault should be injected into
        :type component: Component
        """

        raise NotImplementedError()

    @abstractmethod
    def resolve_fault(self, component: Component):
        """resolves the previously injected fault

        :param component: the component with the injected fault
        :type component: Component
        """

        raise NotImplementedError()

    def next_tick(self, tick: int):
        """handle the next tick event accordingly

        :param tick: the current simulation tick
        :type tick: int
        """
        if tick == self.start_tick:
            self.inject_fault(self.component)
        elif tick == self.end_tick:
            self.resolve_fault(self.component)


class FaultConfiguration(BaseModel):
    """Class that contains the attributes of the Fault class"""

    start_tick = BigIntegerField()
    end_tick = BigIntegerField()
    component: Component = None
    # - affected_element_ID: int = None // has to be implemented in subclasses
    description = TextField(default="injected Fault")
