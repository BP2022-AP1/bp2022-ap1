import hashlib

import pytest

from src import create_app
from src.implementor.models import Token


@pytest.fixture(name="app")
def fixture_app():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    return app


@pytest.fixture(name="client")
def fixture_client(app):
    return app.test_client()


@pytest.fixture(name="clear_admin_token")
def fixture_clear_hashed_token():
    return "token"


@pytest.fixture(name="admin_token", autouse=True)
def fixture_admin_token(clear_admin_token):
    hashed_token = hashlib.sha256(clear_admin_token.encode()).hexdigest()
    name = "admin"
    permission = "admin"
    return Token.create(name=name, permission=permission, hashedToken=hashed_token)


@pytest.fixture(name="clear_token")
def fixture_not_hashed_token():
    return "token"


@pytest.fixture(name="token", autouse=True)
def fixture_token(clear_token):
    hashed_token = hashlib.sha256(clear_token.encode()).hexdigest()
    name = "user"
    permission = "user"
    return Token.create(name=name, permission=permission, hashedToken=hashed_token)
