import uuid

import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiColeDemandSchedule:
    """
    Test the /schedule/cole-demand endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get(
            "/schedule/cole-demand", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {
                "schedule_type": "TrainSchedule",
                "demand_strategy_power_station": "power_station",
                "demand_strategy_scaling_factor": 2,
                "demand_strategy_start_datetime": "2022-01-01T00:00:00+00:00",
                "platforms": ["platform1", "platform2"],
            },
            {
                "schedule_type": "TrainSchedule",
                "demand_strategy_power_station": "power_station",
                "demand_strategy_scaling_factor": 2,
                "demand_strategy_start_datetime": "2022-01-01T00:00:00+00:00",
                "strategy_start_tick": 1,
                "strategy_end_tick": 100,
                "train_schedule_train_type": "passenger",
                "platforms": ["platform1", "platform2"],
            },
        ],
    )
    def test_post(self, client, clear_token, data):
        response = client.post(
            "/schedule/cole-demand", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/schedule/cole-demand", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/schedule/cole-demand/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/schedule/cole-demand/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404
