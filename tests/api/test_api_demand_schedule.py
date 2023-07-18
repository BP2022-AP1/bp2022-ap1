import datetime
import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiCoalDemandSchedule:
    """
    Test the /schedule/coal-demand endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.schedule, "get_all_schedule_ids", mock)
        response = client.get(
            "/schedule/coal-demand", headers={TOKEN_HEADER: clear_token}
        )
        assert mock.call_args.args == (
            {
                "simulationId": None,
                "strategy": "coal-demand",
            },
            token,
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "data, expected_data",
        [
            [
                {
                    "schedule_type": "TrainSchedule",
                    "demand_strategy_power_station": "power_station",
                    "demand_strategy_scaling_factor": 2.0,
                    "demand_strategy_start_datetime": "2022-01-01T00:00:00+00:00",
                    "platforms": ["platform1", "platform2"],
                },
                {
                    "schedule_type": "TrainSchedule",
                    "demand_strategy_power_station": "power_station",
                    "demand_strategy_scaling_factor": 2.0,
                    "demand_strategy_start_datetime": datetime.datetime(
                        2022,
                        1,
                        1,
                        0,
                        0,
                        tzinfo=datetime.timezone(datetime.timedelta(0), "+0000"),
                    ),
                    "platforms": ["platform1", "platform2"],
                },
            ],
            [
                {
                    "schedule_type": "TrainSchedule",
                    "demand_strategy_power_station": "power_station",
                    "demand_strategy_scaling_factor": 2.0,
                    "demand_strategy_start_datetime": "2022-01-01T00:00:00+00:00",
                    "strategy_start_tick": 1,
                    "strategy_end_tick": 100,
                    "train_schedule_train_type": "passenger",
                    "platforms": ["platform1", "platform2"],
                },
                {
                    "schedule_type": "TrainSchedule",
                    "demand_strategy_power_station": "power_station",
                    "demand_strategy_scaling_factor": 2.0,
                    "demand_strategy_start_datetime": datetime.datetime(
                        2022,
                        1,
                        1,
                        0,
                        0,
                        tzinfo=datetime.timezone(datetime.timedelta(0), "+0000"),
                    ),
                    "strategy_start_tick": 1,
                    "strategy_end_tick": 100,
                    "train_schedule_train_type": "passenger",
                    "platforms": ["platform1", "platform2"],
                },
            ],
        ],
    )
    def test_post(self, client, clear_token, token, data, expected_data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(impl.schedule, "create_schedule", mock)
        response = client.post(
            "/schedule/coal-demand", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422
        assert mock.call_args.args == (
            expected_data,
            {"strategy": "coal-demand"},
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.schedule, "create_schedule", mock)
        response = client.post(
            "/schedule/coal-demand", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(dict(), 200))
        monkeypatch.setattr(impl.schedule, "get_schedule", mock)
        response = client.get(
            f"/schedule/coal-demand/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 200
        assert mock.call_args.args == (
            {"identifier": str(object_id), "strategy": "coal-demand"},
            token,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(impl.schedule, "delete_schedule", mock)
        response = client.delete(
            f"/schedule/coal-demand/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 204
        assert mock.call_args.args == (
            {"identifier": str(object_id), "strategy": "coal-demand"},
            token,
        )
