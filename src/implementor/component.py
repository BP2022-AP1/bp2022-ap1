# pylint: disable=unused-argument
# pylint: disable=duplicate-code


import peewee

from src.base_model import db
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
)
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
from src.spawner.spawner import SpawnerConfiguration, SpawnerConfigurationXSchedule


def get_all_schedule_blocked_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the schedule-blocked-faul configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all schedule blocked fault configurations of a single simulation configuration
    if "simulationId" in options and options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404
        simulation_configuration = simulation_configurations.get()
        references = (
            simulation_configuration.schedule_blocked_fault_configuration_references
        )
        # Return all schedule blocked fault configurations
        configs = [
            str(reference.schedule_blocked_fault_configuration.id)
            for reference in references
        ]
        return configs, 200

    configs = [str(config.id) for config in ScheduleBlockedFaultConfiguration.select()]
    return configs, 200


def create_schedule_blocked_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    config = ScheduleBlockedFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_schedule_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = ScheduleBlockedFaultConfiguration.select().where(
        ScheduleBlockedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    return config.to_dict(), 200


def delete_schedule_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = ScheduleBlockedFaultConfiguration.select().where(
        ScheduleBlockedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()

    if config.simulation_configuration_references.exists():
        return (
            "Schedule blocked fault configuration is referenced by a simulation configuration",
            400,
        )

    config.delete_instance()
    return "Deleted schedule-blocked-fault configuration", 204


def get_all_track_blocked_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the track-blocked-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all track blocked fault configurations of a single simulation configuration
    if "simulationId" in options and options["simulationId"] is not None:
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
        # Return all track blocked fault configurations
        configs = [
            str(reference.track_blocked_fault_configuration.id)
            for reference in references
        ]
        return configs, 200

    # Return all track blocked fault configurations
    configs = [str(config.id) for config in TrackBlockedFaultConfiguration.select()]
    return configs, 200


def create_track_blocked_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    config = TrackBlockedFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_track_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrackBlockedFaultConfiguration.select().where(
        TrackBlockedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    return config.to_dict(), 200


def delete_track_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrackBlockedFaultConfiguration.select().where(
        TrackBlockedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()

    if config.simulation_configuration_references.exists():
        return (
            "Track blocked fault configuration is referenced by a simulation configuration",
            400,
        )

    config.delete_instance()
    return "Deleted track-blocked-fault configuration", 204


def get_all_track_speed_limit_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the track-speed-limit-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all track speed limit fault configurations of a single simulation configuration
    if "simulationId" in options and options["simulationId"] is not None:
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

    config = TrackSpeedLimitFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_track_speed_limit_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrackSpeedLimitFaultConfiguration.select().where(
        TrackSpeedLimitFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    return config.to_dict(), 200


def delete_track_speed_limit_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrackSpeedLimitFaultConfiguration.select().where(
        TrackSpeedLimitFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()

    if config.simulation_configuration_references.exists():
        return (
            "Track speed limit fault configuration is referenced by a simulation configuration",
            400,
        )

    config.delete_instance()
    return "Deleted track-speed-limit-fault configuration", 204


def get_all_train_prio_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the train-prio-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all train prio fault configurations of a single simulation configuration
    if "simulationId" in options and options["simulationId"] is not None:
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

    configs = [str(config.id) for config in TrainPrioFaultConfiguration.select()]
    return configs, 200


def create_train_prio_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    config = TrainPrioFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_train_prio_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrainPrioFaultConfiguration.select().where(
        TrainPrioFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    return config.to_dict(), 200


def delete_train_prio_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrainPrioFaultConfiguration.select().where(
        TrainPrioFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()

    if config.simulation_configuration_references.exists():
        return (
            "Train prio fault configuration is referenced by a simulation configuration",
            400,
        )

    config.delete_instance()
    return "Deleted train-prio-fault configuration", 204


def get_all_train_speed_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the train-speed-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all train speed fault configurations of a single simulation configuration
    if "simulationId" in options and options["simulationId"] is not None:
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

    config = TrainSpeedFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_train_speed_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrainSpeedFaultConfiguration.select().where(
        TrainSpeedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    return config.to_dict(), 200


def delete_train_speed_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = TrainSpeedFaultConfiguration.select().where(
        TrainSpeedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()

    if config.simulation_configuration_references.exists():
        return (
            "Train speed fault configuration is referenced by a simulation configuration",
            400,
        )

    config.delete_instance()
    return "Deleted train-speed-fault configuration", 204


def get_all_platform_blocked_fault_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the train-speed-fault configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all platform blocked fault configurations of a single simulation configuration
    if "simulationId" in options and options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404
        simulation_configuration = simulation_configurations.get()
        references = (
            simulation_configuration.platform_blocked_fault_configuration_references
        )
        # Return all platform blocked fault configurations
        configs = [
            str(reference.platform_blocked_fault_configuration.id)
            for reference in references
        ]
        return configs, 200

    # Return all platform blocked fault configurations
    configs = [str(config.id) for config in PlatformBlockedFaultConfiguration.select()]
    return configs, 200


def create_platform_blocked_fault_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    config = PlatformBlockedFaultConfiguration.create(**body)
    return (
        {
            "id": config.id,
        },
        201,
    )


def get_platform_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = PlatformBlockedFaultConfiguration.select().where(
        PlatformBlockedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    return config.to_dict(), 200


def delete_platform_blocked_fault_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    identifier = options["identifier"]
    configs = PlatformBlockedFaultConfiguration.select().where(
        PlatformBlockedFaultConfiguration.id == identifier
    )
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()

    if config.simulation_configuration_references.exists():
        return (
            "Platform blocked fault configuration is referenced by a simulation configuration",
            400,
        )

    config.delete_instance()
    return "Deleted platform-blocked-fault configuration", 204


# -----------------------------------------------------------------------------------
# --------------- INTERLOCKING  CONFIGURATION IS TEMPORARILY DISABLED ---------------
# -----------------------------------------------------------------------------------
# def get_all_interlocking_configuration_ids(options, token):
#     """
#     :param options: A dictionary containing all the parameters for the Operations
#         options["simulationId"]: Specify id of simulation
#             if you only want to get the interlocking configuration of a single simulation
#         :param token: Token object of the current user

#     """

#     # Implement your business logic here
#     # All the parameters are present in the options argument

#     return json.dumps(""), 501  # 200


# def create_interlocking_configuration(body, token):
#     """

#     :param body: The parsed body of the request
#     :param token: Token object of the current user
#     """

#     # Implement your business logic here
#     # All the parameters are present in the options argument

#     return (
#         json.dumps(
#             {
#                 "id": "<uuid>",
#             }
#         ),
#         501,  # 201,
#     )


# def get_interlocking_configuration(options, token):
#     """
#     :param options: A dictionary containing all the parameters for the Operations
#         options["id"]
#     :param token: Token object of the current user

#     """

#     # Implement your business logic here
#     # All the parameters are present in the options argument

#     return json.dumps("<map>"), 501  # 200


# def delete_interlocking_configuration(options, token):
#     """
#     :param options: A dictionary containing all the parameters for the Operations
#         options["id"]
#     :param token: Token object of the current user

#     """

#     # Implement your business logic here
#     # All the parameters are present in the options argument

#     return "", 501  # 204


def get_all_spawner_configuration_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["simulationId"]: Specify id of simulation
            if you only want to get the spawner configuration of a single simulation
        :param token: Token object of the current user

    """

    # Return all spawner configurations of a single simulation configuration
    if options["simulationId"] is not None:
        simulation_id = options["simulationId"]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )
        if not simulation_configurations.exists():
            return "Simulation not found", 404
        simulation_configuration = simulation_configurations.get()
        references = simulation_configuration.spawner_configuration_references
        # Return all platform blocked fault configurations
        configs = [str(reference.spawner_configuration.id) for reference in references]
        return configs, 200

    # Return all spawner configurations
    configs = [str(config.id) for config in SpawnerConfiguration.select()]
    return configs, 200


def create_spawner_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    try:
        with db.atomic():
            config = SpawnerConfiguration()
            config.save()
            for spawner in body["schedule"]:
                SpawnerConfigurationXSchedule.create(
                    spawner_configuration_id=config, schedule_configuration_id=spawner
                )
            return (
                {
                    "id": config.id,
                },
                201,
            )
    except peewee.IntegrityError as error:
        print(error)
        return "Schedule not found", 404


def get_spawner_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """
    config_id = options["identifier"]
    configs = SpawnerConfiguration.select().where(SpawnerConfiguration.id == config_id)
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    config_data = config.to_dict()
    schedules = [
        str(reference.schedule_configuration_id.id)
        for reference in config.schedule_configuration_references
    ]

    return {**config_data, "schedule": schedules}, 200


def delete_spawner_configuration(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    config_id = options["identifier"]
    configs = SpawnerConfiguration.select().where(SpawnerConfiguration.id == config_id)
    if not configs.exists():
        return "Id not found", 404
    config = configs.get()
    if config.simulation_configuration_references.exists():
        return (
            "Spawner configuration is referenced by a simulation configuration",
            400,
        )
    try:
        with db.atomic():
            for reference in config.schedule_configuration_references:
                reference.delete_instance()
            config.delete_instance()

        return "Deleted spawner", 204
    except peewee.IntegrityError:
        return "Something went wrong", 500
