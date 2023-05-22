from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api import schemas
from src.api.decorators import token_required

bp = Blueprint("schedule", __name__)


@bp.route("/schedule", methods=["get"])
@token_required()
def get_all_schedule_ids(token):
    """Get all schedule id"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.schedule.get_all_schedule_ids(options, token)


@bp.route("/schedule", methods=["post"])
@token_required()
def create_schedule(token):
    """Create a schedule"""
    schema = schemas.ScheduleConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.schedule.create_schedule(body, token)


@bp.route("/schedule/<identifier>", methods=["get"])
@token_required()
def get_schedule(identifier, token):
    """Get a schedule"""
    options = {}
    options["identifier"] = identifier

    return impl.schedule.get_schedule(options, token)


@bp.route("/schedule/<identifier>", methods=["delete"])
@token_required()
def delete_schedule(identifier, token):
    """Delete a schedule"""
    options = {}
    options["identifier"] = identifier

    return impl.schedule.delete_schedule(options, token)
