import uuid


class TestApiScheduleBlockedFault:
    """
    Test the /component/fault-injection/schedule-blocked-fault endpoint
    """

    def test_get_all(self, client):
        response = client.get("/component/fault-injection/schedule-blocked-fault")
        assert response.status_code == 501

    def test_post(self, client):
        response = client.post("/component/fault-injection/schedule-blocked-fault")
        assert response.status_code == 501

    def test_get_single(self, client):
        object_id = uuid.uuid4()
        response = client.get(
            f"/component/fault-injection/schedule-blockedfault/{object_id}"
        )
        assert response.status_code == 501

    def test_update(self, client):
        object_id = uuid.uuid4()
        response = client.put(
            f"/component/fault-injection/schedule-blockedfault/{object_id}"
        )
        assert response.status_code == 501

    def test_delete(self, client):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/component/fault-injection/schedule-blockedfault/{object_id}"
        )
        assert response.status_code == 501
