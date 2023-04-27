import uuid

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiTrainPrioFault:
    """
    Test the /component/fault-injection/train-prio-fault endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get(
            "/component/fault-injection/train-prio-fault",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501

    def test_post(self, client, clear_token):
        response = client.post(
            "/component/fault-injection/train-prio-fault",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(
            f"/component/fault-injection/train-prio-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/component/fault-injection/train-prio-fault/{object_id}",
            headers={TOKEN_HEADER: clear_token},
        )
        assert response.status_code == 501
