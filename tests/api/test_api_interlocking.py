# -----------------------------------------------------------------------------------
# --------------- INTERLOCKING  CONFIGURATION IS TEMPORARILY DISABLED ---------------
# -----------------------------------------------------------------------------------
# import uuid

# import pytest

# TOKEN_HEADER = "bp2022-ap1-api-key"


# class TestApiInterlocking:
#     """
#     Test the /component/interlocking endpoint
#     """

#     def test_get_all(self, client, clear_token):
#         response = client.get(
#             "/component/interlocking", headers={TOKEN_HEADER: clear_token}
#         )
#         assert response.status_code == 501

#     @pytest.mark.parametrize("data", [{}, {"dynamicRouting": True}])
#     def test_post(self, client, clear_token, data):
#         response = client.post(
#             "/component/interlocking", headers={TOKEN_HEADER: clear_token}, json=data
#         )
#         assert response.status_code != 422

#     @pytest.mark.parametrize("data", [])
#     def test_post_invalid(self, client, clear_token, data):
#         response = client.post(
#             "/component/interlocking", headers={TOKEN_HEADER: clear_token}, json=data
#         )
#         assert response.status_code == 422

#     def test_get_single(self, client, clear_token):
#         object_id = uuid.uuid4()
#         response = client.get(
#             f"/component/interlocking/{object_id}", headers={TOKEN_HEADER: clear_token}
#         )
#         assert response.status_code == 501

#     def test_delete(self, client, clear_token):
#         object_id = uuid.uuid4()
#         response = client.delete(
#             f"/component/interlocking/{object_id}", headers={TOKEN_HEADER: clear_token}
#         )
#         assert response.status_code == 501
