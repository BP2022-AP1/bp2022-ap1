# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import json


def get_all_simulation_ids(token):
    """
    Get all simulation ids

    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 501  # 200


def create_simulation_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return (
        json.dumps(
            {
                "id": "<uuid>",
            }
        ),
        501,  # 201,
    )


def get_simulation_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def update_simulation_configuration(options, body, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 200


def delete_simulation_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204
