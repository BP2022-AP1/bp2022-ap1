import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl
from tests.api.utils import verify_delete_schedule, verify_get_single_schedule

TOKEN_HEADER = "bp2022-ap1-api-key"

# pylint: disable=duplicate-code


class TestApiRegularSchedule:
    """
    Test the /schedule/regular endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.schedule, "get_all_schedule_ids", mock)
        response = client.get("/schedule/regular", headers={TOKEN_HEADER: clear_token})
        assert mock.call_args.args == (
            {
                "simulationId": None,
                "strategy": "regular",
            },
            token,
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {
                "schedule_type": "TrainSchedule",
                "regular_strategy_frequency": 100,
                "platforms": ["platform1", "platform2"],
            },
            {
                "schedule_type": "TrainSchedule",
                "regular_strategy_frequency": 100,
                "strategy_start_tick": 1,
                "strategy_end_tick": 100,
                "train_schedule_train_type": "passenger",
                "platforms": ["platform1", "platform2"],
            },
        ],
    )
    def test_post(self, client, clear_token, data, token, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(impl.schedule, "create_schedule", mock)
        response = client.post(
            "/schedule/regular", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 201
        assert mock.call_args.args == (
            data,
            {"strategy": "regular"},
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=(uuid.uuid4(), 200))
        monkeypatch.setattr(impl.schedule, "create_schedule", mock)
        response = client.post(
            "/schedule/regular", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=({}, 200))
        monkeypatch.setattr(impl.schedule, "get_schedule", mock)
        verify_get_single_schedule(
            client,
            "schedule/regular",
            clear_token,
            token,
            mock,
            "regular",
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(impl.schedule, "delete_schedule", mock)
        verify_delete_schedule(
            client,
            "schedule/regular",
            clear_token,
            token,
            mock,
            "regular",
        )
