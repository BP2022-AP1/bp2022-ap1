import marshmallow as marsh
from peewee import IntegerField, TextField

from src.fault_injector.fault_types.fault import Fault, FaultConfiguration
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Track


class TrackSpeedLimitFault(Fault):
    """A fault affecting the speed limit of tracks."""

    configuration: "TrackSpeedLimitFaultConfiguration"
    old_speed_limit: float
    track: Track
    wrapper: SimulationObjectUpdatingComponent
    interlocking: IInterlockingDisruptor

    def __init__(
        self,
        configuration,
        logger: Logger,
        wrapper: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        super().__init__(configuration, logger)
        self.wrapper = wrapper
        self.interlocking = interlocking

    def inject_fault(self):
        """inject TrackSpeedLimitFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        self.track: Track = [
            track
            for track in self.wrapper.tracks
            if track.identifier == self.configuration.affected_element_id
        ][0]
        self.old_speed_limit = self.track.max_speed
        self.track.max_speed = self.configuration.new_speed_limit

        self.interlocking.insert_track_speed_limit_changed(
            self.track.identifier
        )
        self.logger.inject_track_speed_limit_fault(self.configuration.id, self.track.identifier, self.old_speed_limit, self.configuration.new_speed_limit)

        # - get track object
        # - save the current speed limit of the track in old_speed_limit
        # - set track speed limit to new_speed_limit

    def resolve_fault(self):
        """resolves the previously injected fault

        :param component: the component with the injected TrackSpeedLimitFault
        :type component: Component
        """
        self.track.max_speed = self.old_speed_limit
        self.interlocking.insert_track_speed_limit_changed(
            self.track.identifier
        )

        self.logger.resolve_track_speed_limit_fault(self.configuration.id)

        # - get track object
        # - set the track speed limit to old_speed_limit


class TrackSpeedLimitFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackSpeedLimitFault class"""

    class Schema(FaultConfiguration.Schema):
        """Schema for TrackSpeedLimitFaultConfiguration"""

        affected_element_id = marsh.fields.String()
        new_speed_limit = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrackSpeedLimitFaultConfiguration":
            return TrackSpeedLimitFaultConfiguration(**data)

    affected_element_id = TextField()
    new_speed_limit = IntegerField(null=False)
