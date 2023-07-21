import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl
from tests.api.utils import verify_delete, verify_get_single

TOKEN_HEADER = "bp2022-ap1-api-key"

# pylint: disable=duplicate-code


class TestApiSpawner:
    """
    Test the /component/spawner endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.component, "get_all_spawner_configuration_ids", mock)
        response = client.get("/component/spawner", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200
        assert mock.call_args.args == ({"simulationId": None}, token)

    @pytest.mark.parametrize("data", [{"schedule": [str(uuid.uuid4())]}])
    def test_post(self, client, clear_token, token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.component,
            "create_spawner_configuration",
            mock,
        )
        response = client.post(
            "/component/spawner", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 201
        expected_data = {
            "schedule": [uuid.UUID(identifier) for identifier in data["schedule"]],
        }
        assert mock.call_args.args == (
            expected_data,
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.component,
            "create_spawner_configuration",
            mock,
        )
        response = client.post(
            "/component/spawner", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=({}, 200))
        monkeypatch.setattr(
            impl.component,
            "get_spawner_configuration",
            mock,
        )
        verify_get_single(
            client,
            "component/spawner",
            clear_token,
            token,
            mock,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(
            impl.component,
            "delete_spawner_configuration",
            mock,
        )
        verify_delete(
            client,
            "component/spawner",
            clear_token,
            token,
            mock,
        )
