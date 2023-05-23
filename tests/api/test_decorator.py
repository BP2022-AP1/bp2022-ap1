import pytest

TOKEN_HEADER = "bp2022-ap1-api-key"


@pytest.mark.parametrize(
    "route, response_code",
    [
        ("/run", 200),
        ("/simulation", 200),
        ("/component/interlocking", 501),
        ("/component/spawner", 200),
        ("/component/fault-injection/schedule-blocked-fault", 200),
        ("/component/fault-injection/platform-blocked-fault", 200),
        ("/component/fault-injection/track-blocked-fault", 200),
        ("/component/fault-injection/train-prio-fault", 200),
        ("/component/fault-injection/train-speed-fault", 200),
        ("/component/fault-injection/track-speed-limit-fault", 200),
        ("/run/00000000-0000-0000-0000-000000000000", 404),
        ("/simulation/00000000-0000-0000-0000-000000000000", 404),
        ("/component/interlocking/00000000-0000-0000-0000-000000000000", 501),
        ("/component/spawner/00000000-0000-0000-0000-000000000000", 404),
        (
            "/component/fault-injection/schedule-blocked-fault/00000000-0000-0000-0000-000000000000",
            404,
        ),
        (
            "/component/fault-injection/platform-blocked-fault/00000000-0000-0000-0000-000000000000",
            404,
        ),
        (
            "/component/fault-injection/track-blocked-fault/00000000-0000-0000-0000-000000000000",
            404,
        ),
        (
            "/component/fault-injection/train-prio-fault/00000000-0000-0000-0000-000000000000",
            404,
        ),
        (
            "/component/fault-injection/train-speed-fault/00000000-0000-0000-0000-000000000000",
            404,
        ),
        (
            "/component/fault-injection/track-speed-limit-fault/00000000-0000-0000-0000-000000000000",
            404,
        ),
    ],
)
class TestApiDecoratorTokenRequired:
    """
    Test the @token_required decorator
    """

    # response_code is only relevant for valid tokens
    # pylint: disable-next=unused-argument
    def test_no_token(self, client, route, response_code):
        response = client.get(route)
        assert response.status_code == 401

    # response_code is only relevant for valid tokens
    # pylint: disable-next=unused-argument
    def test_invalid_token(self, client, route, response_code):
        invalid_clear_token = "invalid"
        response = client.get(route, headers={TOKEN_HEADER: invalid_clear_token})
        assert response.status_code == 401

    def test_valid_token(self, client, route, response_code, clear_token):
        response = client.get(route, headers={TOKEN_HEADER: clear_token})
        assert response.status_code == response_code
