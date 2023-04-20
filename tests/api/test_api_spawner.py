import uuid


class TestApiSpawner:
    """
    Test the /component/spawner endpoint
    """

    def test_get_all(self, client):
        response = client.get("/component/spawner")
        assert response.status_code == 501

    def test_post(self, client):
        response = client.post("/component/spawner")
        assert response.status_code == 501

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/component/spawner/{object_id}")
        assert response.status_code == 501

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/component/spawner/{object_id}")
        assert response.status_code == 501
