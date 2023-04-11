from flask import Blueprint, request
from marshmallow import Schema, fields
from webargs.flaskparser import parser

from .. import impl
from ..schemas import model

bp = Blueprint("simulation", __name__)


@bp.route("/simulation", methods=["get"])
def GetAllSimulationId():
    return impl.simulation.GetAllSimulationId()


@bp.route("/simulation", methods=["post"])
def CreateSimulationConfiguration():
    schema = model.SimulationConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.simulation.CreateSimulationConfiguration(body)


@bp.route("/simulation/<id>", methods=["get"])
def GetSimulationConfiguration(id):
    options = {}
    options["id"] = id

    return impl.simulation.GetSimulationConfiguration(options)


@bp.route("/simulation/<id>", methods=["put"])
def UpdateSimulationConfiguration(id):
    options = {}
    options["id"] = id

    schema = model.SimulationConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.simulation.UpdateSimulationConfiguration(options, body)


@bp.route("/simulation/<id>", methods=["delete"])
def DeleteSimulationConfiguration(id):
    options = {}
    options["id"] = id

    return impl.simulation.DeleteSimulationConfiguration(options)
