import hashlib
from functools import wraps

from flask import request

from src.implementor.models import Token

TOKEN_HEADER = "bp2022-ap1-api-key"


def token_required(func):
    """Decorator for token authentication"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        token_clear = request.headers.get(TOKEN_HEADER)
        if not token_clear:
            return {"message": "Token is missing"}, 401
        token_hash = hashlib.sha256(token_clear.encode()).hexdigest()
        token = Token.select().where(Token.hashedToken == token_hash).first()
        if not token:
            return {"message": "Token is invalid"}, 401
        return func(*args, **kwargs, token=token)

    return decorated_function
