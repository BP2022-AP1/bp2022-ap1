import json


def GetAllScheduleIds(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation if you only want to get all schedules of a single simulation

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 200


def CreateSchedule(body):
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


def GetSchedule(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 200


def UpdateSchedule(options, body):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    :param body: The parsed body of the request
    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 204


def DeleteSchedule(options):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 204
