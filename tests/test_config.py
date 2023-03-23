import os

import dotenv
import pytest


@pytest.fixture
def mock_dotenv(monkeypatch):
    """
    Mock dotenv to return self defined environment file content.
    """

    mocked_shared_env = {"v1": "shared", "v2": "shared"}
    mocked_secret_env = {"v1": "secret"}

    def add_env_from_dict(env_dict: dict[str, str | None]) -> None:
        for key, value in env_dict.items():
            os.environ[key] = value

    def load_dotenv_mock(env_file: str) -> dict[str, str | None]:
        match env_file:
            case ".env.shared":
                add_env_from_dict(mocked_shared_env)
            case ".env.secret":
                add_env_from_dict(mocked_secret_env)

    monkeypatch.setattr(dotenv, "load_dotenv", load_dotenv_mock)


def test_env_variables_import_order(
    mock_dotenv,
):  # pylint: disable=redefined-outer-name,unused-argument
    """
    Test if the loading order of the environment variables are correct.
    os can be overwritten by .env.secret and .env.shared.
    .env.shared can be overwritten by .env.secret.
    .env.secret cannot be overwritten.
    """
    # pylint: disable-next=import-outside-toplevel,unused-import
    import src.config

    assert os.getenv("v1") == "secret"
    assert os.getenv("v2") == "shared"
