import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiRandomSchedule:
    """
    Test the /schedule/random endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.schedule, "get_all_schedule_ids", mock)
        response = client.get("/schedule/random", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200
        assert mock.call_args.args == (
            {
                "simulationId": None,
                "strategy": "random",
            },
            token,
        )

    @pytest.mark.parametrize(
        "data",
        [
            {
                "schedule_type": "TrainSchedule",
                "random_strategy_trains_per_1000_ticks": 0.1,
                "random_strategy_seed": 1,
                "platforms": ["platform1", "platform2"],
            },
            {
                "schedule_type": "TrainSchedule",
                "random_strategy_trains_per_1000_ticks": 0.1,
                "random_strategy_seed": 1,
                "strategy_start_tick": 1,
                "strategy_end_tick": 100,
                "train_schedule_train_type": "passenger",
                "platforms": ["platform1", "platform2"],
            },
        ],
    )
    def test_post(self, client, clear_token, token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(impl.schedule, "create_schedule", mock)
        response = client.post(
            "/schedule/random", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422
        assert mock.call_args.args == (
            data,
            {"strategy": "random"},
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=(uuid.uuid4(), 200))
        monkeypatch.setattr(impl.schedule, "create_schedule", mock)
        response = client.post(
            "/schedule/random", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(dict(), 200))
        monkeypatch.setattr(impl.schedule, "get_schedule", mock)
        response = client.get(
            f"/schedule/random/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 200
        assert mock.call_args.args == (
            {"identifier": str(object_id), "strategy": "random"},
            token,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(impl.schedule, "delete_schedule", mock)
        response = client.delete(
            f"/schedule/random/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 204
        assert mock.call_args.args == (
            {"identifier": str(object_id), "strategy": "random"},
            token,
        )
