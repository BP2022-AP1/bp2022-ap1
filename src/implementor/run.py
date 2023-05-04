# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import json

from src.implementor.models import Run, SimulationConfiguration, Token


def get_all_run_ids(options: dict, token: Token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]
    :param token: Token object of the current user

    """

    # Return all runs of a single simulation configuration
    simulation_configuration_key = "simulationId"
    if (
        simulation_configuration_key in options
        and options[simulation_configuration_key] is not None
    ):
        simulation_id = options[simulation_configuration_key]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )

        if not simulation_configurations.exists():
            return "Simulation not found", 404

        simulation_configuration = simulation_configurations.get()
        runs = simulation_configuration.runs

        runs_string = [str(run.id) for run in runs]
        return runs_string, 200

    runs = [str(run.id) for run in Run.select()]
    return runs, 200


def create_run(body, token):
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


def get_run(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_run(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204
