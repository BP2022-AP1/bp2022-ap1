# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import hashlib
import secrets

from src.implementor.models import Token


def create_token(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument
    token = secrets.token_hex(32)
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    Token.create(**body, hashedToken=hashed_token)

    return {"token": token}, 201
