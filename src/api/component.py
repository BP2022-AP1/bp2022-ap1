from flask import Blueprint, request
from marshmallow import Schema, fields
from webargs.flaskparser import parser

from .. import impl
from ..schemas import model

bp = Blueprint("component", __name__)


@bp.route("/component/fault-injection/schedule-blocked-fault", methods=["get"])
def GetScheduleBlockedFaultConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetScheduleBlockedFaultConfigurationIds(options)


@bp.route("/component/fault-injection/schedule-blocked-fault", methods=["post"])
def CreateScheduleBlockedFaultConfiguration():
    schema = model.ScheduleBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateScheduleBlockedFaultConfiguration(body)


@bp.route("/component/fault-injection/schedule-blockedfault/<id>", methods=["get"])
def GetScheduleBlockedFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetScheduleBlockedFaultConfiguration(options)


@bp.route("/component/fault-injection/schedule-blockedfault/<id>", methods=["put"])
def UpdateScheduleBlockedFaultConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.ScheduleBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateScheduleBlockedFaultConfiguration(options, body)


@bp.route("/component/fault-injection/schedule-blockedfault/<id>", methods=["delete"])
def DeleteScheduleBlockedFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteScheduleBlockedFaultConfiguration(options)


@bp.route("/component/fault-injection/track-blocked-fault", methods=["get"])
def GetTrackBlockedFaultConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetTrackBlockedFaultConfigurationIds(options)


@bp.route("/component/fault-injection/track-blocked-fault", methods=["post"])
def CreateTrackBlockedFaultConfiguration():
    schema = model.TrackBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateTrackBlockedFaultConfiguration(body)


@bp.route("/component/fault-injection/track-blocked-fault/<id>", methods=["get"])
def GetTrackBlockedFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetTrackBlockedFaultConfiguration(options)


@bp.route("/component/fault-injection/track-blocked-fault/<id>", methods=["put"])
def UpdateTrackBlockedFaultConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.TrackBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateTrackBlockedFaultConfiguration(options, body)


@bp.route("/component/fault-injection/track-blocked-fault/<id>", methods=["delete"])
def DeleteTrackBlockedFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteTrackBlockedFaultConfiguration(options)


@bp.route("/component/fault-injection/track-speed-limit-fault", methods=["get"])
def GetTrackSpeedLimitFaultConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetTrackSpeedLimitFaultConfigurationIds(options)


@bp.route("/component/fault-injection/track-speed-limit-fault", methods=["post"])
def CreateTrackSpeedLimitFaultConfiguration():
    schema = model.TrackSpeedLimitFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateTrackSpeedLimitFaultConfiguration(body)


@bp.route("/component/fault-injection/track-split-limit-fault/<id>", methods=["get"])
def GetTrackSpeedLimitFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetTrackSpeedLimitFaultConfiguration(options)


@bp.route("/component/fault-injection/track-split-limit-fault/<id>", methods=["put"])
def UpdateTrackSpeedLimitFaultConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.TrackSpeedLimitFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateTrackSpeedLimitFaultConfiguration(options, body)


@bp.route("/component/fault-injection/track-split-limit-fault/<id>", methods=["delete"])
def DeleteTrackSpeedLimitFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteTrackSpeedLimitFaultConfiguration(options)


@bp.route("/component/fault-injection/train-prio-fault", methods=["get"])
def GetTrainPrioFaultConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetTrainPrioFaultConfigurationIds(options)


@bp.route("/component/fault-injection/train-prio-fault", methods=["post"])
def CreateTrainPrioFaultConfiguration():
    schema = model.TrainPrioFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateTrainPrioFaultConfiguration(body)


@bp.route("/component/fault-injection/train-prio-fault/<id>", methods=["get"])
def GetTrainPrioFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetTrainPrioFaultConfiguration(options)


@bp.route("/component/fault-injection/train-prio-fault/<id>", methods=["put"])
def UpdateTrainPrioFaultConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.TrainPrioFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateTrainPrioFaultConfiguration(options, body)


@bp.route("/component/fault-injection/train-prio-fault/<id>", methods=["delete"])
def DeleteTrainPrioFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteTrainPrioFaultConfiguration(options)


@bp.route("/component/fault-injection/train-speed-fault", methods=["get"])
def GetTrainSpeedFaultConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetTrainSpeedFaultConfigurationIds(options)


@bp.route("/component/fault-injection/train-speed-fault", methods=["post"])
def CreateTrainSpeedFaultConfiguration():
    schema = model.TrainSpeedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateTrainSpeedFaultConfiguration(body)


@bp.route("/component/fault-injection/train-speed-fault/<id>", methods=["get"])
def GetTrainSpeedFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetTrainSpeedFaultConfiguration(options)


@bp.route("/component/fault-injection/train-speed-fault/<id>", methods=["put"])
def UpdateTrainSpeedFaultConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.TrainSpeedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateTrainSpeedFaultConfiguration(options, body)


@bp.route("/component/fault-injection/train-speed-fault/<id>", methods=["delete"])
def DeleteTrainSpeedFaultConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteTrainSpeedFaultConfiguration(options)


@bp.route("/component/interlocking", methods=["get"])
def GetInterlockingConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetInterlockingConfigurationIds(options)


@bp.route("/component/interlocking", methods=["post"])
def CreateInterlockingConfiguration():
    schema = model.InterlockingConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateInterlockingConfiguration(body)


@bp.route("/component/interlocking/<id>", methods=["get"])
def GetInterlockingConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetInterlockingConfiguration(options)


@bp.route("/component/interlocking/<id>", methods=["put"])
def UpdateInterlockingConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.InterlockingConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateInterlockingConfiguration(options, body)


@bp.route("/component/interlocking/<id>", methods=["delete"])
def DeleteInterlockingConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteInterlockingConfiguration(options)


@bp.route("/component/spawner", methods=["get"])
def GetSpawnerConfigurationIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.GetSpawnerConfigurationIds(options)


@bp.route("/component/spawner", methods=["post"])
def CreateSpawnerConfiguration():
    schema = model.SpawnerConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.CreateSpawnerConfiguration(body)


@bp.route("/component/spawner/<id>", methods=["get"])
def GetSpawnerConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.GetSpawnerConfiguration(options)


@bp.route("/component/spawner/<id>", methods=["put"])
def UpdateSpawnerConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.SpawnerConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.UpdateSpawnerConfiguration(options, body)


@bp.route("/component/spawner/<id>", methods=["delete"])
def DeleteSpawnerConfiguration(id):
    options = {}
    options["id"] = id

    return impl.component.DeleteSpawnerConfiguration(options)
