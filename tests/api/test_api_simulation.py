import uuid

import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiSimulation:
    """
    Test the /simulation endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get("/simulation", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {"spawner": uuid.uuid4()},
            {
                "spawner": uuid.uuid4(),
                "description": "test-description",
                "platform_blocked_fault": [uuid.uuid4()],
                "schedule_blocked_fault": [uuid.uuid4()],
                "track_blocked_fault": [uuid.uuid4()],
                "track_speed_limit_fault": [uuid.uuid4()],
                "train_speed_fault": [uuid.uuid4()],
                "train_prio_fault": [uuid.uuid4()],
            },
        ],
    )
    def test_post(self, client, clear_token, data):
        response = client.post(
            "/simulation", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/simulation", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/simulation/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "data",
        [
            {},
            {
                "spawner": uuid.uuid4(),
                "description": "test-description",
                "platform_blocked_fault": [uuid.uuid4()],
                "schedule_blocked_fault": [uuid.uuid4()],
                "track_blocked_fault": [uuid.uuid4()],
                "track_speed_limit_fault": [uuid.uuid4()],
                "train_speed_fault": [uuid.uuid4()],
                "train_prio_fault": [uuid.uuid4()],
            },
        ],
    )
    def test_update(self, client, clear_token, data):
        object_id = uuid.uuid4()
        response = client.put(
            f"/simulation/{object_id}", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 404

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/simulation/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 404
