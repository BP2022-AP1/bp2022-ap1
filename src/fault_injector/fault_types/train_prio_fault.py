import marshmallow as marsh
from peewee import IntegerField, TextField

from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfiguration


class TrainPrioFault(Fault):
    """A fault affecting the priority of trains."""

    def inject_fault(self, component: Component):
        """inject TrainPrioFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        # - get train object
        # - save the current prio of the train in old_prio
        # - set train prio to new_prio
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        """resolves the previously injected TrainPrioFault

        :param component: the component with the injected fault
        :type component: Component
        """
        # - get train object
        # - set the train prio to old_prio

        raise NotImplementedError()


class TrainPrioFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrainPrioFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrainCancelledFaultConfiguration"""

        affected_element_id = marsh.fields.String()
        new_prio = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrainPrioFaultConfiguration":
            return TrainPrioFaultConfiguration(**data)

    affected_element_id = TextField()
    new_prio = IntegerField(null=False)
