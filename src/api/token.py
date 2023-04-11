from flask import Blueprint, request
from webargs.flaskparser import parser

from .. import implementor as impl
from ..schemas import model

bp = Blueprint("token", __name__)


@bp.route("/token", methods=["post"])
def create_token():
    """Create a token"""
    schema = model.TokenConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.token.create_token(body)
