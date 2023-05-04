import uuid

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiSchedule:
    """
    Test the /schedule endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get("/schedule", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 501

    def test_post(self, client, clear_token):
        response = client.post("/schedule", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 501

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
