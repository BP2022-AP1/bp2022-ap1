from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.schemas import model

bp = Blueprint("simulation", __name__)


@bp.route("/simulation", methods=["get"])
def get_all_simulation_ids():
    """Get all simulation id"""
    return impl.simulation.get_all_simulation_ids()


@bp.route("/simulation", methods=["post"])
def create_simulation_configuration():
    """Create a simulation configuration"""
    schema = model.SimulationConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.simulation.create_simulation_configuration(body)


@bp.route("/simulation/<identifier>", methods=["get"])
def get_simulation_configuration(identifier):
    """Get a simulation configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.simulation.get_simulation_configuration(options)


@bp.route("/simulation/<identifier>", methods=["put"])
def update_simulation_configuration(identifier):
    """Update a simulation configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.SimulationConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.simulation.update_simulation_configuration(options, body)


@bp.route("/simulation/<identifier>", methods=["delete"])
def delete_simulation_configuration(identifier):
    """Delete a simulation configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.simulation.delete_simulation_configuration(options)
