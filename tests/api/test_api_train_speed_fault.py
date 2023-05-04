import uuid
import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiTrainSpeedFault:
    """
    Test the /component/fault-injection/train-speed-fault endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get(
            "/component/fault-injection/train-speed-fault",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501

    @pytest.mark.parametrize(
        "data",
        [
            {"new_speed": 0.1, "affected_element_id": "test"},
            {
                "affected_element_id": "test",
                "new_speed": 0.1,
                "start_tick": 1,
                "end_tick": 2,
                "inject_probability": 0.5,
                "resolve_probability": 0.5,
                "description": "test",
                "strategy": "test",
            },
        ],
    )
    def test_post(self, client, clear_token, data):
        response = client.post(
            "/component/fault-injection/train-speed-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/component/fault-injection/train-speed-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/component/fault-injection/train-speed-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/component/fault-injection/train-speed-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501
