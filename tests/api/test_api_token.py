import uuid
import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiToken:
    """
    Test the /token endpoint
    """

    @pytest.mark.parametrize("data", [{"name": "user", "permission": "admin"}])
    def test_post(self, client, clear_token, data):
        response = client.post("/token", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code == 501

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post("/token", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code == 422

    def test_get_all(self, client, clear_token):
        response = client.get("/token", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 405  # route not available for  get

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/token/{object_id}")
        assert response.status_code == 404  # route not available

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/token/{object_id}")
        assert response.status_code == 404  # route not available
