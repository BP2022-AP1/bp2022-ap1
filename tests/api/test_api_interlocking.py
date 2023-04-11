import uuid


class TestApiInterlocking:
    """
    Test the /component/interlocking endpoint
    """

    def test_get_all(self, client):
        response = client.get("/component/interlocking")
        assert response.status_code == 200

    def test_post(self, client):
        response = client.post("/component/interlocking")
        assert response.status_code == 201

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/component/interlocking/{object_id}")
        assert response.status_code == 200

    def test_update(self, client):
        object_id = uuid.uuid4()
        response = client.put(f"/component/interlocking/{object_id}")
        assert response.status_code == 204

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/component/interlocking/{object_id}")
        assert response.status_code == 204
