import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl
from tests.api.utils import verify_delete, verify_get_single

TOKEN_HEADER = "bp2022-ap1-api-key"

# pylint: disable=duplicate-code


class TestApiTrackSpeedLimitFault:
    """
    Test the /component/fault-injection/track-speed-limit-fault endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(
            impl.component, "get_all_track_speed_limit_fault_configuration_ids", mock
        )
        response = client.get(
            "/component/fault-injection/track-speed-limit-fault",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 200
        assert mock.call_args.args == (
            {"simulationId": None},
            token,
        )

    @pytest.mark.parametrize(
        "data",
        [
            {
                "new_speed_limit": 1,
                "description": "test",
                "strategy": "test",
                "affected_element_id": "test",
            },
            {
                "affected_element_id": "test",
                "new_speed_limit": 1,
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
            "create_track_speed_limit_fault_configuration",
            mock,
        )
        response = client.post(
            "/component/fault-injection/track-speed-limit-fault",
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
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.component,
            "create_track_speed_limit_fault_configuration",
            mock,
        )
        response = client.post(
            "/component/fault-injection/track-speed-limit-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=({}, 200))
        monkeypatch.setattr(
            impl.component, "get_track_speed_limit_fault_configuration", mock
        )
        verify_get_single(
            client,
            "component/fault-injection/track-speed-limit-fault",
            clear_token,
            token,
            mock,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(
            impl.component, "delete_track_speed_limit_fault_configuration", mock
        )
        verify_delete(
            client,
            "component/fault-injection/track-speed-limit-fault",
            clear_token,
            token,
            mock,
        )
