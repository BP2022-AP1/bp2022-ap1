import json


def GetAllRunId(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 200


def CreateRun(body):
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


def GetRun(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 200


def DeleteRun(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 204
