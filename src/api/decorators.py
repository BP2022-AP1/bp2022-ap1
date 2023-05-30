from functools import wraps

from flask import request

from src.implementor.models import Token
from src.implementor.permission import Permission
from src.implementor.token import hash_token

TOKEN_HEADER = "bp2022-ap1-api-key"


def token_required(permission: Permission = None):
    """Decorator for token authentication"""

    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            token_clear = request.headers.get(TOKEN_HEADER)
            if not token_clear:
                return {"message": "Token is missing"}, 401
            token_hash = hash_token(token_clear)
            token = Token.select().where(Token.hashedToken == token_hash).first()
            if not token:
                return {"message": "Token is invalid"}, 401
            if permission and token.permission != permission.value:
                return {"message": "Permission is missing"}, 403
            return func(*args, **kwargs, token=token)

        return decorated_function

    return decorator
