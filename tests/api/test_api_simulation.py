import uuid
from unittest.mock import Mock

import pytest

from src import implementor as impl

TOKEN_HEADER = "bp2022-ap1-api-key"


def get_expected_data(data, exception=list()):
    expected_data = dict()
    for key, val in data.items():
        if key in exception:
            expected_data[key] = val
        elif isinstance(val, list):
            expected_data[key] = [uuid.UUID(v) for v in val]
        else:
            expected_data[key] = uuid.UUID(val)
    return expected_data


class TestApiSimulation:
    """
    Test the /simulation endpoint
    """

    def test_get_all(self, client, clear_token, token, monkeypatch):
        mock = Mock(return_value=([uuid.uuid4()], 200))
        monkeypatch.setattr(impl.simulation, "get_all_simulation_ids", mock)
        response = client.get("/simulation", headers={TOKEN_HEADER: clear_token})
        assert response.status_code == 200
        assert mock.call_args.args == (token,)

    @pytest.mark.parametrize(
        "data",
        [
            {"spawner": str(uuid.uuid4())},
            {
                "spawner": str(uuid.uuid4()),
                "description": "test-description",
                "platform_blocked_fault": [str(uuid.uuid4())],
                "schedule_blocked_fault": [str(uuid.uuid4())],
                "track_blocked_fault": [str(uuid.uuid4())],
                "track_speed_limit_fault": [str(uuid.uuid4())],
                "train_speed_fault": [str(uuid.uuid4())],
                "train_prio_fault": [str(uuid.uuid4())],
            },
        ],
    )
    def test_post(self, client, clear_token, token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.simulation,
            "create_simulation_configuration",
            mock,
        )
        response = client.post(
            "/simulation", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 201
        expected_data = get_expected_data(data, ["description"])
        assert mock.call_args.args == (
            expected_data,
            token,
        )

    @pytest.mark.parametrize("data", [{}])
    def test_post_invalid(self, client, clear_token, data, monkeypatch):
        mock = Mock(return_value=({"id": uuid.uuid4()}, 201))
        monkeypatch.setattr(
            impl.simulation,
            "create_simulation_configuration",
            mock,
        )
        response = client.post(
            "/simulation", headers={TOKEN_HEADER: clear_token}, json=data
        )
        assert response.status_code == 422
        assert not mock.called

    def test_get_single(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(dict(), 200))
        monkeypatch.setattr(impl.simulation, "get_simulation_configuration", mock)
        response = client.get(
            f"/simulation/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 200
        assert mock.call_args.args == (
            {"identifier": str(object_id)},
            token,
        )

    @pytest.mark.parametrize(
        "data",
        [
            {},
            {
                "spawner": str(uuid.uuid4()),
                "description": "test-description",
                "platform_blocked_fault": [str(uuid.uuid4())],
                "schedule_blocked_fault": [str(uuid.uuid4())],
                "track_blocked_fault": [str(uuid.uuid4())],
                "track_speed_limit_fault": [str(uuid.uuid4())],
                "train_speed_fault": [str(uuid.uuid4())],
                "train_prio_fault": [str(uuid.uuid4())],
            },
        ],
    )
    def test_update(self, client, clear_token, token, data, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(dict(), 200))
        monkeypatch.setattr(impl.simulation, "update_simulation_configuration", mock)
        response = client.put(
            f"/simulation/{object_id}", headers={TOKEN_HEADER: clear_token}, json=data
        )

        expected_data = get_expected_data(data, exception=["description"])
        assert response.status_code == 200
        assert mock.call_args.args == (
            {"identifier": str(object_id)},
            expected_data,
            token,
        )

    def test_delete(self, client, clear_token, token, monkeypatch):
        object_id = uuid.uuid4()
        mock = Mock(return_value=(str(), 204))
        monkeypatch.setattr(impl.simulation, "delete_simulation_configuration", mock)
        response = client.delete(
            f"/simulation/{object_id}", headers={TOKEN_HEADER: clear_token}
        )
        assert response.status_code == 204
        assert mock.call_args.args == (
            {"identifier": str(object_id)},
            token,
        )
