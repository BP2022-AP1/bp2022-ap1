from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api import schemas
from src.api.decorators import token_required

bp = Blueprint("schedule", __name__)


@bp.route("/schedule/regular", methods=["get"])
@token_required
def get_all_schedule_ids(token):
    """Get all schedule id"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")
    options["strategy"] = "regular"

    return impl.schedule.get_all_schedule_ids(options, token)


@bp.route("/schedule/regular", methods=["post"])
@token_required
def create_schedule(token):
    """Create a schedule"""
    schema = schemas.RegularScheduleConfiguration()

    body = parser.parse(schema, request, location="json")

    options = {}
    options["strategy"] = "regular"

    return impl.schedule.create_schedule(body, options, token)


@bp.route("/schedule/regular/<identifier>", methods=["get"])
@token_required
def get_schedule(identifier, token):
    """Get a schedule"""
    options = {}
    options["identifier"] = identifier
    options["strategy"] = "regular"

    return impl.schedule.get_schedule(options, token)


@bp.route("/schedule/regular/<identifier>", methods=["delete"])
@token_required
def delete_schedule(identifier, token):
    """Delete a schedule"""
    options = {}
    options["identifier"] = identifier
    options["strategy"] = "regular"

    return impl.schedule.delete_schedule(options, token)
