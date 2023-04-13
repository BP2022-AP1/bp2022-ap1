import pytest

from src import create_app


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
