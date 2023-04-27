import marshmallow as marsh
from peewee import ForeignKeyField, TextField

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


class ScheduleBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the ScheduleBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for ScheduleBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "ScheduleBlockedFaultConfiguration":
            return ScheduleBlockedFaultConfiguration(**data)

    affected_element_id = TextField()


class ScheduleBlockedFaultConfigurationXSimulationConfiguration(BaseModel):
    """Reference table class for m:n relation
    between ScheduleBlockedFaultConfiguration and SimulationConfiguration."""

    class Schema(BaseModel.Schema):
        """Marshmallow schema for ScheduleBlockedFaultConfigurationXSimulationConfiguration"""

        simulation_configuration = marsh.fields.UUID(required=True)
        schedule_blocked_fault_configuration = marsh.fields.UUID(required=True)

        def _make(
            self, data: dict
        ) -> "ScheduleBlockedFaultConfigurationXSimulationConfiguration":
            """Constructs a ScheduleBlockedFaultConfigurationXSimulationConfiguration
            from a dictionary.

                :param data: The dictionary.
                :return: A ScheduleBlockedFaultConfigurationXSimulationConfiguration.
            """
            return ScheduleBlockedFaultConfigurationXSimulationConfiguration(**data)

    simulation_configuration = ForeignKeyField(
        SimulationConfiguration,
        null=False,
        backref="schedule_blocked_fault_configuration_references",
    )
    schedule_blocked_fault_configuration = ForeignKeyField(
        ScheduleBlockedFaultConfiguration,
        null=False,
        backref="simulation_configuration_references",
    )
