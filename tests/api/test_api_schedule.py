import uuid
import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiSchedule:
    """
    Test the /schedule endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get("/schedule", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 501

    @pytest.mark.parametrize(
        "data",
        [
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RegularScheduleStrategy",
            },
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RegularScheduleStrategy",
                "strategy_start_tick": 1,
                "strategy_end_tick": 100,
                "train_schedule_train_type": "passenger",
                "regular_strategy_frequency": 100,
                "random_strategy_trains_per_1000_ticks": 0.1,
                "random_strategy_seed": 1,
                "demand_strategy_power_station": "power_station",
                "demand_strategy_scaling_factor": 2,
                "demand_strategy_start_datetime": "2022-01-01T00:00:00+00:00",
            },
        ],
    )
    def test_post(self, client, clear_token, data):
        response = client.post(
            "/schedule", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/schedule", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/schedule/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 501

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/schedule/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 501
