from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api import schemas
from src.api.decorators import token_required

bp = Blueprint("simulation", __name__)


@bp.route("/simulation", methods=["get"])
@token_required
def get_all_simulation_ids(token):
    """Get all simulation id"""
    return impl.simulation.get_all_simulation_ids(token)


@bp.route("/simulation", methods=["post"])
@token_required
def create_simulation_configuration(token):
    """Create a simulation configuration"""
    schema = schemas.SimulationConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.simulation.create_simulation_configuration(body, token)


@bp.route("/simulation/<identifier>", methods=["get"])
@token_required
def get_simulation_configuration(identifier, token):
    """Get a simulation configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.simulation.get_simulation_configuration(options, token)


@bp.route("/simulation/<identifier>", methods=["put"])
@token_required
def update_simulation_configuration(identifier, token):
    """Update a simulation configuration"""
    options = {}
    options["identifier"] = identifier

    schema = schemas.SimulationConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.simulation.update_simulation_configuration(options, body, token)


@bp.route("/simulation/<identifier>", methods=["delete"])
@token_required
def delete_simulation_configuration(identifier, token):
    """Delete a simulation configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.simulation.delete_simulation_configuration(options, token)
