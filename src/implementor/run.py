# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import json


def get_all_run_id(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 200


def create_run(body):
    """

    :param body: The parsed body of the request
    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return (
        json.dumps(
            {
                "id": "<uuid>",
            }
        ),
        201,
    )


def get_run(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 200


def delete_run(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 204
