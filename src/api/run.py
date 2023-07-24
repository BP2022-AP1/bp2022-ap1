from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api import schemas
from src.api.decorators import token_required

bp = Blueprint("run", __name__)


@bp.route("/run", methods=["get"])
def get_all_run_ids():
    """Get all run id"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.run.get_all_run_ids(options, None)


@bp.route("/run", methods=["post"])
def create_run():
    """Create a run"""
    schema = schemas.RunConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.run.create_run(body, None)


@bp.route("/run/<identifier>", methods=["get"])
def get_run(identifier):
    """Get a run"""
    options = {}
    options["identifier"] = identifier

    return impl.run.get_run(options, None)


@bp.route("/run/<identifier>", methods=["delete"])
def delete_run(identifier):
    """Delete a run"""
    options = {}
    options["identifier"] = identifier

    return impl.run.delete_run(options, None)
