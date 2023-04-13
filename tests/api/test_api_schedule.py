import uuid


class TestApiSchedule:
    """
    Test the /schedule endpoint
    """

    def test_get_all(self, client):
        response = client.get("/schedule")
        assert response.status_code == 501

    def test_post(self, client):
        response = client.post("/schedule")
        assert response.status_code == 501

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/schedule/{object_id}")
        assert response.status_code == 501

    def test_update(self, client):
        object_id = uuid.uuid4()
        response = client.put(f"/schedule/{object_id}")
        assert response.status_code == 501

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/schedule/{object_id}")
        assert response.status_code == 501
