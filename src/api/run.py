from flask import Blueprint, request
from marshmallow import Schema, fields
from webargs.flaskparser import parser

from .. import impl
from ..schemas import model

bp = Blueprint("run", __name__)


@bp.route("/run", methods=["get"])
def GetAllRunId():
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.run.GetAllRunId(options)


@bp.route("/run", methods=["post"])
def CreateRun():
    schema = model.RunConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.run.CreateRun(body)


@bp.route("/run/<id>", methods=["get"])
def GetRun(id):
    options = {}
    options["id"] = id

    return impl.run.GetRun(options)


@bp.route("/run/<id>", methods=["delete"])
def DeleteRun(id):
    options = {}
    options["id"] = id

    return impl.run.DeleteRun(options)
