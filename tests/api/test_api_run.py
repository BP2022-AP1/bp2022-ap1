import uuid


class TestApiRun:
    """
    Test the /run endpoint
    """

    def test_get_all(self, client):
        response = client.get("/run")
        assert response.status_code == 501

    def test_post(self, client):
        response = client.post("/run")
        assert response.status_code == 501

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(f"/run/{object_id}")
        assert response.status_code == 501

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(f"/run/{object_id}")
        assert response.status_code == 501
