import marshmallow as marsh
from peewee import IntegerField, TextField

from src.component import Component
from src.fault_injector.fault_types.fault import Fault, FaultConfiguration
from src.wrapper.simulation_object_updating_component import SimulationObjectUpdatingComponent
from src.wrapper.simulation_objects import Track
from src.interlocking_component.route_controller import IInterlockingDisruptor
from logger.logger import Logger


class TrackSpeedLimitFault(Fault):
    """A fault affecting the speed limit of tracks."""

    configuration: "TrackSpeedLimitFaultConfiguration"
    old_speed_limit: int

    def inject_fault(self, component: Component):
        """inject TrackSpeedLimitFault into the given component

        :param component: The component the fault should be injected into
        :type component: Component
        """
        track: Track = [track for track in self.configuration.wrapper_component.tracks() if track.id == self.configuration.affected_element_id][0]
        self.old_speed_limit = track.max_speed
        track.max_speed = self.configuration.new_speed_limit

        self.configuration.interlocking_component.insert_track_speed_limit_changed(self.configuration.affected_element_id)
        # self.configuration.logger.inject_fault

        
        # - get track object
        # - save the current speed limit of the track in old_speed_limit
        # - set track speed limit to new_speed_limit
        raise NotImplementedError()

    def resolve_fault(self, component: Component):
        """resolves the previously injected fault

        :param component: the component with the injected TrackSpeedLimitFault
        :type component: Component
        """
        # - get track object
        # - set the track speed limit to old_speed_limit

        raise NotImplementedError()


class TrackSpeedLimitFaultConfiguration(FaultConfiguration):
    """Class that contains the attributes of the TrackSpeedLimitFault class"""

    def __init__(self, logger: Logger, wrapper: SimulationObjectUpdatingComponent, interlocking: IInterlockingDisruptor):
        super().__init__(logger)
        self.wrapper_component = wrapper
        self.interlocking_component = interlocking


    class Schema(FaultConfiguration.Schema):
        """Schema for TrackSpeedLimitFaultConfiguration"""

        affected_element_id = marsh.fields.String()
        new_speed_limit = marsh.fields.Integer(required=True)

        def _make(self, data: dict) -> "TrackSpeedLimitFaultConfiguration":
            return TrackSpeedLimitFaultConfiguration(**data)

    wrapper_component: SimulationObjectUpdatingComponent
    interlocking_component: IInterlockingDisruptor
    affected_element_id = TextField()
    new_speed_limit = IntegerField(null=False)
