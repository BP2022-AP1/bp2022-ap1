from flask import Blueprint, request
from marshmallow import Schema, fields
from webargs.flaskparser import parser

from .. import impl
from ..schemas import model

bp = Blueprint("schedule", __name__)


@bp.route("/schedule", methods=["get"])
def GetAllScheduleIds():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.schedule.GetAllScheduleIds(options)


@bp.route("/schedule", methods=["post"])
def CreateSchedule():
    schema = Schedule.Schema()

    body = parser.parse(schema, request, location="json")

    return impl.schedule.CreateSchedule(body)


@bp.route("/schedule/<id>", methods=["get"])
def GetSchedule(id):
    options = {}
    options["id"] = id

    return impl.schedule.GetSchedule(options)


@bp.route("/schedule/<id>", methods=["put"])
def UpdateSchedule(id):
    options = {}
    options["id"] = id

    schema = model.Schedule()

    body = parser.parse(schema, request, location="json")

    return impl.schedule.UpdateSchedule(options, body)


@bp.route("/schedule/<id>", methods=["delete"])
def DeleteSchedule(id):
    options = {}
    options["id"] = id

    return impl.schedule.DeleteSchedule(options)
