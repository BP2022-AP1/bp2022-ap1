import marshmallow as marsh
from peewee import TextField

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)


class ScheduleBlockedFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the ScheduleBlockedFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for ScheduleBlockedFaultConfiguration"""

        affected_element_id = marsh.fields.String()

        def _make(self, data: dict) -> "ScheduleBlockedFaultConfiguration":
            return ScheduleBlockedFaultConfiguration(**data)

    affected_element_id = TextField()
