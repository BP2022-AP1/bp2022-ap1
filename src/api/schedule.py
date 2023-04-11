from flask import Blueprint, request
from webargs.flaskparser import parser

from .. import implementor as impl
from ..schemas import model

bp = Blueprint("schedule", __name__)


@bp.route("/schedule", methods=["get"])
def get_all_schedule_ids():
    """Get all schedule id"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.schedule.get_all_schedule_ids(options)


@bp.route("/schedule", methods=["post"])
def create_schedule():
    """Create a schedule"""
    schema = model.Schedule()

    body = parser.parse(schema, request, location="json")

    return impl.schedule.create_schedule(body)


@bp.route("/schedule/<identifier>", methods=["get"])
def get_schedule(identifier):
    """Get a schedule"""
    options = {}
    options["identifier"] = identifier

    return impl.schedule.get_schedule(options)


@bp.route("/schedule/<identifier>", methods=["put"])
def update_schedule(identifier):
    """Update a schedule"""
    options = {}
    options["identifier"] = identifier

    schema = model.Schedule()

    body = parser.parse(schema, request, location="json")

    return impl.schedule.update_schedule(options, body)


@bp.route("/schedule/<identifier>", methods=["delete"])
def delete_schedule(identifier):
    """Delete a schedule"""
    options = {}
    options["identifier"] = identifier

    return impl.schedule.delete_schedule(options)
