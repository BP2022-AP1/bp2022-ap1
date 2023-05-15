import uuid

import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiScheduleBlockedFault:
    """
    Test the /component/fault-injection/schedule-blocked-fault endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get(
            "/component/fault-injection/schedule-blocked-fault",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 200

    @pytest.mark.parametrize(
        "data",
        [
            {"affected_element_id": "test", "description": "test", "strategy": "test"},
            {
                "affected_element_id": "test",
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
            "/component/fault-injection/schedule-blocked-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post(
            "/component/fault-injection/schedule-blocked-fault",
            headers={TOKEN_HEADER: clear_token},
            json=data,
        )
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/component/fault-injection/schedule-blocked-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/component/fault-injection/schedule-blocked-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501
