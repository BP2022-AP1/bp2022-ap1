from flask import Blueprint, request
from marshmallow import Schema, fields
from webargs.flaskparser import parser

from .. import impl
from ..schemas import model

bp = Blueprint("token", __name__)


@bp.route("/token", methods=["post"])
def CreateToken():
    schema = model.TokenConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.token.CreateToken(body)
