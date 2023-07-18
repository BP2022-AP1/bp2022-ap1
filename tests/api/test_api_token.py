import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl
from src.implementor.permission import Permission

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiToken:
    """
    Test the /token endpoint
    """

    @pytest.mark.parametrize(
        "data, expected_data",
        [
            [
                {"name": "user", "permission": "admin"},
                {"name": "user", "permission": Permission.ADMIN},
            ],
            [
                {"name": "user", "permission": "user"},
                {"name": "user", "permission": Permission.USER},
            ],
        ],
    )
    def test_post(
        self, client, clear_admin_token, admin_token, data, expected_data, monkeypatch
    ):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.token,
            "create_token",
            mock,
        )
        response = client.post(
            "/token", headers={TOKEN_HEADER: clear_admin_token}, json=data
        )
        assert response.status_code == 201
        assert mock.call_args.args == (expected_data, admin_token)

    @pytest.mark.parametrize("data", [{"name": "user", "permission": "user"}])
    def test_post_no_permission(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.token,
            "create_token",
            mock,
        )
        response = client.post("/token", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code == 403
        assert not mock.called

    @pytest.mark.parametrize("data", [{}, {"name": "user"}, {"permission": "invalid"}])
    def test_post_invalid(self, client, clear_admin_token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.token,
            "create_token",
            mock,
        )
        response = client.post(
            "/token", headers={TOKEN_HEADER: clear_admin_token}, json=data
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_all(self, client, clear_admin_token):
        response = client.get("/token", headers={TOKEN_HEADER: clear_admin_token})
        assert response.status_code == 405  # route not available for  get

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/token/{object_id}")
        assert response.status_code == 404  # route not available

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/token/{object_id}")
        assert response.status_code == 404  # route not available
