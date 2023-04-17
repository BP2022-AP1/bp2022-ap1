from marshmallow import Schema, fields

# ------------------------------- #
# THIS FILE WILL BE REMOVED LATER #
# ------------------------------- #


class CreateInterlockingConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateRunInlineResp(Schema):
    id = fields.UUID()


class CreateScheduleBlockedFaultConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateScheduleInlineResp(Schema):
    id = fields.UUID()


class CreateSimulationConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateSpawnerConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateTrackBlockedFaultConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateTrackSpeedLimitFaultConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateTrainPrioFaultConfigurationInlineResp(Schema):
    id = fields.UUID()


class CreateTrainSpeedFaultConfigurationInlineResp(Schema):
    id = fields.UUID()


class GetAllRunIdInlineResp(Schema):
    pass


class GetAllScheduleIdsInlineResp(Schema):
    pass


class GetAllSimulationIdInlineResp(Schema):
    pass


class GetInterlockingConfigurationIdsInlineResp(Schema):
    pass


class GetScheduleBlockedFaultConfigurationIdsInlineResp(Schema):
    pass


class GetSpawnerConfigurationIdsInlineResp(Schema):
    pass


class GetTrackBlockedFaultConfigurationIdsInlineResp(Schema):
    pass


class GetTrackSpeedLimitFaultConfigurationIdsInlineResp(Schema):
    pass


class GetTrainPrioFaultConfigurationIdsInlineResp(Schema):
    pass


class GetTrainSpeedFaultConfigurationIdsInlineResp(Schema):
    pass


class InterlockingConfiguration(Schema):
    pass


class RunConfiguration(Schema):
    pass


class RunStatus(Schema):
    pass


class Schedule(Schema):
    pass


class ScheduleBlockedFaultConfiguration(Schema):
    pass


class SimulationConfiguration(Schema):
    pass


class SpawnerConfiguration(Schema):
    pass


class Token(Schema):
    pass


class TokenConfiguration(Schema):
    permission = fields.String()


class TrackBlockedFaultConfiguration(Schema):
    pass


class TrackSpeedLimitFaultConfiguration(Schema):
    pass


class TrainPrioFaultConfiguration(Schema):
    pass


class TrainSpeedFaultConfiguration(Schema):
    pass


class PlatformBlockedFaultConfiguration(Schema):
    pass
