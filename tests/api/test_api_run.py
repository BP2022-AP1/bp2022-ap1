import uuid

import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


class TestApiRun:
    """
    Test the /run endpoint
    """

    def test_get_all(self, client, clear_token):
        response = client.get("/run", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200

    @pytest.mark.parametrize("data", [{"simulation_configuration": str(uuid.uuid4())}])
    def test_post(self, client, clear_token, data):
        response = client.post("/run", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code != 422

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data):
        response = client.post("/run", headers={TOKEN_HEADER: clear_token}, json=data)
        assert response.status_code == 422

    def test_get_single(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.get(f"/run/{object_id}", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 501

    def test_delete(self, client, clear_token):
        object_id = uuid.uuid4()
        response = client.delete(
            f"/run/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 501
