import os

import dotenv
import pytest


@pytest.fixture
def mock_dotenv(monkeypatch):
    """
    Mock dotenv to return self defined environment file content.
    """

    def dotenv_values_mock(env_file: str) -> dict[str, str | None]:
        match env_file:
            case ".env.shared":
                return {"v1": "shared", "v2": "shared", "v3": "shared"}
            case ".env.secret":
                return {"v1": "secret", "v2": "secret"}
            case ".env.test":
                return {"v1": "test", "v2": "test"}

    monkeypatch.setattr(dotenv, "dotenv_values", dotenv_values_mock)


@pytest.fixture
def mock_os(monkeypatch):
    """
    Mock environment variables imported from os to return self defined environment variables.
    """

    mock_environ = {"v1": "os"}
    monkeypatch.setattr(os, "environ", mock_environ)


def test_env_variables_import_order(
    mock_dotenv, mock_os
):  # pylint: disable=redefined-outer-name,unused-argument
    """
    Test if the loading order of the environment variables are correct.
    .env.shared can be overwritten by .env.secret and os.
    .env.secret can be overwritten by os.
    os cannot be overwritten.
    """

    from src.constants import constants

    assert constants["v1"] == "os"
    assert constants["v2"] == "secret"
    assert constants["v3"] == "shared"


def test_test_env_variable_import_order(
    mock_dotenv, mock_os
):  # pylint: disable=redefined-outer-name,unused-argument
    """
    Test if the loading order of the test environment variables are correct.
    .env.test can be overwritten by os.
    os cannot be overwritten.
    """
    from constants import constants

    assert constants["v1"] == "os"
    assert constants["v2"] == "test"
