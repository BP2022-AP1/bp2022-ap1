import uuid

import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiRegularSchedule:
    """
    Test the /schedule/regular endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get("/schedule/regular", headers={TOKEN_HEADER: clear_token})
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
    def test_post(self, client, clear_token, data):
        response = client.post(
            "/schedule/regular", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/schedule/regular", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/schedule/regular/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/schedule/regular/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404
