from abc import ABC, abstractmethod

import marshmallow as marsh
from peewee import IntegerField, TextField

from src.base_model import BaseModel
from src.logger.logger import Logger


class Fault(ABC):
    """An abstract fault for the fault injection"""

    configuration: "FaultConfiguration"
    logger: Logger

    def __init__(self, configuration, logger: Logger):
        self.configuration = configuration
        self.logger = logger

    @abstractmethod
    def inject_fault(self):
        """injects the fault into the given component

        :param component: the component the fault should be injected into
        :type component: Component
        """

        raise NotImplementedError()

    @abstractmethod
    def resolve_fault(self):
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
        if tick == self.configuration.start_tick:
            self.inject_fault()
        elif tick == self.configuration.end_tick:
            self.resolve_fault()


class FaultConfiguration(BaseModel):
    """Class that contains the attributes of the Fault class"""

    class Schema(BaseModel.Schema):
        """Schema for the FaultConfiguration"""

        start_tick = marsh.fields.Integer(required=True)
        end_tick = marsh.fields.Integer(required=True)
        description = marsh.fields.String()

        def _make(self, data: dict) -> "FaultConfiguration":
            return FaultConfiguration(**data)

    start_tick = IntegerField(null=False)
    end_tick = IntegerField(null=False)

    # - affected_element_ID: int = None // has to be implemented in subclasses
    description = TextField(default="injected Fault")
