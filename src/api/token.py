from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api.decorators import token_required
from src.api import schemas

bp = Blueprint("token", __name__)


@bp.route("/token", methods=["post"])
@token_required
def create_token(token):
    """Create a token"""
    schema = schemas.TokenConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.token.create_token(body, token)
