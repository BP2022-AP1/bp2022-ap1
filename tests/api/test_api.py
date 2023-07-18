import os

from src.implementor.models import Token
from src.implementor.token import hash_token


# Initialization of the database is done when client is called
# pylint: disable=unused-argument
def test_first_token(client):
    clear_token = os.getenv("FIRST_ADMIN_TOKEN")
    hashed_token = hash_token(clear_token)
    assert Token.select().where(Token.hashedToken == hashed_token).exists()
