import uuid


class TestApiToken:
    """
    Test the /token endpoint
    """

    def test_post(self, client):
        response = client.post("/token")
        assert response.status_code == 201

    def test_get_all(self, client):
        response = client.get("/token")
        assert response.status_code == 405  # route not available for  get

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/token/{object_id}")
        assert response.status_code == 404  # route not available

    def test_update(self, client):
        object_id = uuid.uuid4()
        response = client.put(f"/token/{object_id}")
        assert response.status_code == 404  # route not available

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/token/{object_id}")
        assert response.status_code == 404  # route not available
