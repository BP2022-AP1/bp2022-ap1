# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import json

from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.implementor.models import SimulationConfiguration


def get_all_schedule_blocked_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the schedule-blocked-faul configuration of a single simulation
        :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 501  # 200


def create_schedule_blocked_fault_configuration(body, token):
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


def get_schedule_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_schedule_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_track_blocked_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the track-blocked-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all train prio fault configurations of a single simulation configuration
    if options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404
        simulation_configuration = simulation_configurations.get()
        references = (
            simulation_configuration.track_blocked_fault_configuration_references
        )
        # Return all train prio fault configurations
        configs = [
            str(reference.track_blocked_fault_configuration.id)
            for reference in references
        ]
        return configs, 200

    return json.dumps(""), 200


def create_track_blocked_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument
    config = TrackBlockedFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_track_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_track_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_track_speed_limit_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the track-speed-limit-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all track speed limit fault configurations of a single simulation configuration
    if options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404

        simulation_configuration = simulation_configurations.get()
        references = (
            simulation_configuration.track_speed_limit_fault_configuration_references
        )

        configs = [
            str(reference.track_speed_limit_fault_configuration.id)
            for reference in references
        ]
        return configs, 200

    # Return all track speed limit fault configurations
    configs = [str(config.id) for config in TrackSpeedLimitFaultConfiguration.select()]
    return configs, 200


def create_track_speed_limit_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument
    config = TrackSpeedLimitFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_track_speed_limit_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_track_speed_limit_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_train_prio_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the train-prio-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all train prio fault configurations of a single simulation configuration
    if options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404
        simulation_configuration = simulation_configurations.get()
        references = simulation_configuration.train_prio_fault_configuration_references
        # Return all train prio fault configurations
        configs = [
            str(reference.train_prio_fault_configuration.id) for reference in references
        ]
        return configs, 200

    return json.dumps(""), 200


def create_train_prio_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument
    config = TrainPrioFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_train_prio_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_train_prio_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_train_speed_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the train-speed-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all train speed fault configurations of a single simulation configuration
    if options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404
        simulation_configuration = simulation_configurations.get()
        references = simulation_configuration.train_speed_fault_configuration_references

        configs = [
            str(reference.train_speed_fault_configuration.id)
            for reference in references
        ]
        return configs, 200

    # Return all train speed fault configurations
    configs = [str(config.id) for config in TrainSpeedFaultConfiguration.select()]
    return configs, 200


def create_train_speed_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument
    config = TrainSpeedFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_train_speed_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_train_speed_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_platform_blocked_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the train-speed-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 501  # 200


def create_platform_blocked_fault_configuration(body, token):
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


def get_platform_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_platform_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_interlocking_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the interlocking configuration of a single simulation
        :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 501  # 200


def create_interlocking_configuration(body, token):
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


def get_interlocking_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_interlocking_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204


def get_all_spawner_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the spawner configuration of a single simulation
        :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps(""), 501  # 200


def create_spawner_configuration(body, token):
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


def get_spawner_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_spawner_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204
