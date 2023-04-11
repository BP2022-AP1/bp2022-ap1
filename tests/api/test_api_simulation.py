import uuid


class TestApiSimulation:
    """
    Test the /simulation endpoint
    """

    def test_get_all(self, client):
        response = client.get("/simulation")
        assert response.status_code == 200

    def test_post(self, client):
        response = client.post("/simulation")
        assert response.status_code == 201

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/simulation/{object_id}")
        assert response.status_code == 200

    def test_update(self, client):
        object_id = uuid.uuid4()
        response = client.put(f"/simulation/{object_id}")
        assert response.status_code == 204

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/simulation/{object_id}")
        assert response.status_code == 204
