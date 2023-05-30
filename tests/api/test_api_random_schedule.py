import uuid

import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiRandomSchedule:
    """
    Test the /schedule/random endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get("/schedule/random", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200

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
    def test_post(self, client, clear_token, data):
        response = client.post(
            "/schedule/random", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/schedule/random", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/schedule/random/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/schedule/random/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404
