from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api import schemas
from src.api.decorators import token_required

bp = Blueprint("run", __name__)


@bp.route("/run", methods=["get"])
@token_required
def get_all_run_ids(token):
    """Get all run id"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.run.get_all_run_ids(options, token)


@bp.route("/run", methods=["post"])
@token_required
def create_run(token):
    """Create a run"""
    schema = schemas.RunConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.run.create_run(body, token)


@bp.route("/run/<identifier>", methods=["get"])
@token_required
def get_run(identifier, token):
    """Get a run"""
    options = {}
    options["identifier"] = identifier

    return impl.run.get_run(options, token)


@bp.route("/run/<identifier>", methods=["delete"])
@token_required
def delete_run(identifier, token):
    """Delete a run"""
    options = {}
    options["identifier"] = identifier

    return impl.run.delete_run(options, token)
