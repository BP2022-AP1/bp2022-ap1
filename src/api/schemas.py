from marshmallow import Schema, fields

from src.implementor.permission import Permission


class InterlockingConfiguration(Schema):
    """Schema for the InterlockingConfiguration"""

    dynamicRouting = fields.Boolean()


class RunConfiguration(Schema):
    """The marshmallow schema for the run model."""

    simulation_configuration = fields.UUID(required=True)


class ScheduleConfiguration(Schema):
    """The marshmallow schema for every schedule configuration"""

    schedule_type = fields.String(required=True)
    platforms = fields.List(fields.String(), required=True)
    strategy_start_tick = fields.Integer()
    strategy_end_tick = fields.Integer()

    train_schedule_train_type = fields.String()


class RegularScheduleConfiguration(ScheduleConfiguration):
    """The marshmallow schema for the regular schedule configuration"""

    regular_strategy_frequency = fields.Integer(required=True)


class CoalDemandScheduleConfiguration(ScheduleConfiguration):
    """The marshmallow schema for the coal demand schedule configuration"""

    demand_strategy_power_station = fields.String(required=True)
    demand_strategy_scaling_factor = fields.Float(required=True)
    demand_strategy_start_datetime = fields.DateTime(required=True)


class SimulationConfiguration(Schema):
    """The marshmallow schema for the simulation configuration model."""

    description = fields.String()
    spawner = fields.UUID(required=True)
    platform_blocked_fault = fields.List(fields.UUID())
    schedule_blocked_fault = fields.List(fields.UUID())
    track_blocked_fault = fields.List(fields.UUID())
    track_speed_limit_fault = fields.List(fields.UUID())
    train_speed_fault = fields.List(fields.UUID())
    train_prio_fault = fields.List(fields.UUID())


class UpdateSimulationConfiguration(SimulationConfiguration):
    """The marshmallow schema for the simulation configuration model."""

    spawner = fields.UUID()


class SpawnerConfiguration(Schema):
    """The marshmallow schema for the spawner configuration model."""

    schedule = fields.List(fields.UUID(), required=True)


class TokenConfiguration(Schema):
    """The marshmallow schema for the token model."""

    permission = fields.Enum(Permission, required=True, by_value=True)
    name = fields.String(required=True)


class FaultConfiguration(Schema):
    """Schema for the FaultConfiguration"""

    start_tick = fields.Integer()
    end_tick = fields.Integer()
    inject_probability = fields.Float()
    resolve_probability = fields.Float()
    description = fields.String(required=True)
    strategy = fields.String(required=True)


class TrackBlockedFaultConfiguration(FaultConfiguration):
    """Schema for TrackBlockedFaultConfiguration"""

    affected_element_id = fields.String(required=True)


class TrackSpeedLimitFaultConfiguration(FaultConfiguration):
    """Schema for TrackSpeedLimitFaultConfiguration"""

    affected_element_id = fields.String(required=True)
    new_speed_limit = fields.Integer(required=True)


class TrainPrioFaultConfiguration(FaultConfiguration):
    """Schema for TrainPrioFaultConfiguration"""

    affected_element_id = fields.String()
    new_prio = fields.Integer(required=True)


class TrainSpeedFaultConfiguration(FaultConfiguration):
    """Schema for TrainSpeedFaultConfiguration"""

    affected_element_id = fields.String(required=True)
    new_speed = fields.Float(required=True)


class PlatformBlockedFaultConfiguration(FaultConfiguration):
    """Schema for PlatformBlockedFaultConfiguration"""

    affected_element_id = fields.String(required=True)


class ScheduleBlockedFaultConfiguration(FaultConfiguration):
    """Schema for ScheduleBlockedFaultConfiguration"""

    affected_element_id = fields.String(required=True)
