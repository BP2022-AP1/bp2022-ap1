import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl
from tests.api.utils import verify_delete, verify_get_single

TOKEN_HEADER = "bp2022-ap1-api-key"

# pylint: disable=duplicate-code


class TestApiRun:
    """
    Test the /run endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.run, "get_all_run_ids", mock)
        response = client.get("/run", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200
        assert mock.call_args.args == (
            {
                "simulationId": None,
            },
            token,
        )

    @pytest.mark.parametrize("data", [{"simulation_configuration": str(uuid.uuid4())}])
    def test_post(self, client, clear_token, token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(impl.run, "create_run", mock)
        response = client.post("/run", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code == 201
        assert mock.call_args.args == (
            {"simulation_configuration": (uuid.UUID(data["simulation_configuration"]))},
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=(uuid.uuid4(), 200))
        monkeypatch.setattr(impl.run, "create_run", mock)
        response = client.post("/run", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=({}, 200))
        monkeypatch.setattr(impl.run, "get_run", mock)
        verify_get_single(
            client,
            "run",
            clear_token,
            token,
            mock,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(impl.run, "delete_run", mock)
        verify_delete(
            client,
            "run",
            clear_token,
            token,
            mock,
        )
