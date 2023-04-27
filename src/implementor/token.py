# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import json


def create_token(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 201
