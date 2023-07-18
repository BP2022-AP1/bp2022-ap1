import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiPlatformBlockedFault:
    """
    Test the /component/fault-injection/platform-blocked-fault endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(
            impl.component, "get_all_platform_blocked_fault_configuration_ids", mock
        )
        response = client.get(
            "/component/fault-injection/platform-blocked-fault",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 200
        assert mock.call_args.args == (
            {
                "simulationId": None,
            },
            token,
        )

    @pytest.mark.parametrize(
        "data",
        [
            {"affected_element_id": "test", "description": "test", "strategy": "test"},
            {
                "affected_element_id": "test",
                "start_time": 1,
                "end_time": 2,
                "inject_probability": 0.5,
                "resolve_probability": 0.5,
                "description": "test",
                "strategy": "test",
            },
        ],
    )
    def test_post(self, client, clear_token, token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.component,
            "create_platform_blocked_fault_configuration",
            mock,
        )
        response = client.post(
            "/component/fault-injection/platform-blocked-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code == 201
        assert mock.call_args.args == (
            data,
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=(uuid.uuid4(), 200))
        monkeypatch.setattr(
            impl.component, "create_platform_blocked_fault_configuration", mock
        )
        response = client.post(
            "/component/fault-injection/platform-blocked-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(dict(), 200))
        monkeypatch.setattr(
            impl.component, "get_platform_blocked_fault_configuration", mock
        )
        response = client.get(
            f"/component/fault-injection/platform-blocked-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 200
        assert mock.call_args.args == (
            {"identifier": str(object_id)},
            token,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(
            impl.component, "delete_platform_blocked_fault_configuration", mock
        )
        response = client.delete(
            f"/component/fault-injection/platform-blocked-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 204
        assert mock.call_args.args == (
            {"identifier": str(object_id)},
            token,
        )
