import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl
from tests.api.utils import verify_delete, verify_get_single

TOKEN_HEADER = "bp2022-ap1-api-key"

# pylint: disable=duplicate-code


class TestApiTrainPrioFault:
    """
    Test the /component/fault-injection/train-prio-fault endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(
            impl.component, "get_all_train_prio_fault_configuration_ids", mock
        )
        response = client.get(
            "/component/fault-injection/train-prio-fault",
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
                "affected_element_id": "test",
                "new_prio": 1,
                "description": "test",
                "strategy": "test",
            },
            {
                "affected_element_id": "test",
                "new_prio": 1,
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
            "create_train_prio_fault_configuration",
            mock,
        )
        response = client.post(
            "/component/fault-injection/train-prio-fault",
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
            "create_train_prio_fault_configuration",
            mock,
        )
        response = client.post(
            "/component/fault-injection/train-prio-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=({}, 200))
        monkeypatch.setattr(impl.component, "get_train_prio_fault_configuration", mock)
        verify_get_single(
            client,
            "component/fault-injection/train-prio-fault",
            clear_token,
            token,
            mock,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(
            impl.component, "delete_train_prio_fault_configuration", mock
        )
        verify_delete(
            client,
            "component/fault-injection/train-prio-fault",
            clear_token,
            token,
            mock,
        )
