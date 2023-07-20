import uuid

TOKEN_HEADER = "bp2022-ap1-api-key"


def verify_get_single(client, route, clear_token, token, mock):
    object_id = uuid.uuid4()
    response = client.get(f"/{route}/{object_id}", headers={TOKEN_HEADER: clear_token})
    assert response.status_code == 200
    assert mock.call_args.args == (
        {"identifier": str(object_id)},
        token,
    )


def verify_delete(client, route, clear_token, token, mock):
    object_id = uuid.uuid4()
    response = client.delete(
        f"/{route}/{object_id}", headers={TOKEN_HEADER: clear_token}
    )
    assert response.status_code == 204
    assert mock.call_args.args == (
        {"identifier": str(object_id)},
        token,
    )


def verify_get_single_schedule(client, route, clear_token, token, mock, strategy):
    object_id = uuid.uuid4()
    response = client.get(f"/{route}/{object_id}", headers={TOKEN_HEADER: clear_token})
    assert response.status_code == 200
    assert mock.call_args.args == (
        {"identifier": str(object_id), "strategy": strategy},
        token,
    )


def verify_delete_schedule(client, route, clear_token, token, mock, strategy):
    object_id = uuid.uuid4()
    response = client.delete(
        f"/{route}/{object_id}", headers={TOKEN_HEADER: clear_token}
    )
    assert response.status_code == 204
    assert mock.call_args.args == (
        {"identifier": str(object_id), "strategy": strategy},
        token,
    )
