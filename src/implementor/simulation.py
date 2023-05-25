# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import peewee

from src.base_model import BaseModel, db
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfigurationXSimulationConfiguration,
)
from src.implementor.models import SimulationConfiguration
from src.spawner.spawner import SpawnerConfigurationXSimulationConfiguration

platform_blocked_fault = {
    "key": "platform_blocked_fault",
    "column": "platform_blocked_fault_configuration",
}

schedule_blocked_fault = {
    "key": "schedule_blocked_fault",
    "column": "schedule_blocked_fault_configuration",
}

track_blocked_fault = {
    "key": "track_blocked_fault",
    "column": "track_blocked_fault_configuration",
}

track_speed_limit_fault = {
    "key": "track_speed_limit_fault",
    "column": "track_speed_limit_fault_configuration",
}

train_speed_fault = {
    "key": "train_speed_fault",
    "column": "train_speed_fault_configuration",
}

train_prio_fault = {
    "key": "train_prio_fault",
    "column": "train_prio_fault_configuration",
}


def get_all_simulation_ids(token):
    """
    Get all simulation ids

    :param token: Token object of the current user
    """

    simulations = [str(sim.id) for sim in SimulationConfiguration.select()]
    return simulations, 200


def create_simulation_configuration(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    try:
        with db.atomic():
            simulation = SimulationConfiguration()
            simulation.save()

            # Add references between simulation configuration and spawner
            spawner_configuration = body["spawner"]
            SpawnerConfigurationXSimulationConfiguration.create(
                simulation_configuration=simulation,
                spawner_configuration=spawner_configuration,
            )

            # Add references between simulation configuration and platform blocked fault
            check_and_create_configuration_references(
                simulation,
                platform_blocked_fault["key"],
                PlatformBlockedFaultConfigurationXSimulationConfiguration,
                platform_blocked_fault["column"],
                body,
            )

            # Add references between simulation configuration and schedule blocked fault

            check_and_create_configuration_references(
                simulation,
                schedule_blocked_fault["key"],
                ScheduleBlockedFaultConfigurationXSimulationConfiguration,
                schedule_blocked_fault["column"],
                body,
            )

            # Add references between simulation configuration and track blocked fault
            check_and_create_configuration_references(
                simulation,
                track_blocked_fault["key"],
                TrackBlockedFaultConfigurationXSimulationConfiguration,
                track_blocked_fault["column"],
                body,
            )

            # Add references between simulation configuration and track speed limit fault
            check_and_create_configuration_references(
                simulation,
                track_speed_limit_fault["key"],
                TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
                track_speed_limit_fault["column"],
                body,
            )

            # Add references between simulation configuration and train prio fault
            check_and_create_configuration_references(
                simulation,
                train_prio_fault["key"],
                TrainPrioFaultConfigurationXSimulationConfiguration,
                train_prio_fault["column"],
                body,
            )

            # Add references between simulation configuration and train speed fault
            check_and_create_configuration_references(
                simulation,
                train_speed_fault["key"],
                TrainSpeedFaultConfigurationXSimulationConfiguration,
                train_speed_fault["column"],
                body,
            )

            return {"id": str(simulation.id)}, 201

    except peewee.IntegrityError:
        return (
            {"error": "Configuration not found"},
            404,
        )


def get_simulation_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """

    simulation_configuration_id = options["identifier"]
    simulation_configurations = SimulationConfiguration.select().where(
        SimulationConfiguration.id == simulation_configuration_id
    )

    if not simulation_configurations.exists():
        return "Simulation not found", 404

    simulation_configuration = simulation_configurations.get()

    spawner_ids = [
        str(reference.spawner_configuration.id)
        for reference in simulation_configuration.spawner_configuration_references
    ]
    spawner_id = spawner_ids[0]

    platform_blocked_fault_ids = [
        str(reference.platform_blocked_fault_configuration.id)
        for reference in simulation_configuration.platform_blocked_fault_configuration_references
    ]

    schedule_blocked_fault_ids = [
        str(reference.schedule_blocked_fault_configuration.id)
        for reference in simulation_configuration.schedule_blocked_fault_configuration_references
    ]

    track_blocked_fault_ids = [
        str(reference.track_blocked_fault_configuration.id)
        for reference in simulation_configuration.track_blocked_fault_configuration_references
    ]

    track_speed_limit_fault_ids = [
        str(reference.track_speed_limit_fault_configuration.id)
        for reference in simulation_configuration.track_speed_limit_fault_configuration_references
    ]

    train_speed_fault_ids = [
        str(reference.train_speed_fault_configuration.id)
        for reference in simulation_configuration.train_speed_fault_configuration_references
    ]

    train_prio_fault_ids = [
        str(reference.train_prio_fault_configuration.id)
        for reference in simulation_configuration.train_prio_fault_configuration_references
    ]

    return {
        "id": str(simulation_configuration.id),
        "description": simulation_configuration.description,
        "spawner": spawner_id,
        "platform_blocked_fault": platform_blocked_fault_ids,
        "schedule_blocked_fault": schedule_blocked_fault_ids,
        "track_blocked_fault": track_blocked_fault_ids,
        "track_speed_limit_fault": track_speed_limit_fault_ids,
        "train_speed_fault": train_speed_fault_ids,
        "train_prio_fault": train_prio_fault_ids,
    }, 200


def update_simulation_configuration(options, body, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["identifier"]
    :param body: The parsed body of the request
    :param token: Token object of the current user
    """

    simulation_configuration_id = options["identifier"]
    simulation_configurations = SimulationConfiguration.select().where(
        SimulationConfiguration.id == simulation_configuration_id
    )
    if not simulation_configurations.exists():
        return "Run not found", 404

    simulation = simulation_configurations.get()

    if simulation.runs.count() > 0:
        return "Simulation configuration is used in a run", 400

    try:
        with db.atomic():
            if "description" in body:
                SimulationConfiguration.update(description=body["description"]).where(
                    SimulationConfiguration.id == simulation.id
                ).execute()

            # Remove and add references between simulation configuration and spawner if needed
            if "spawner" in body:
                spawner_configuration = body["spawner"]
                SpawnerConfigurationXSimulationConfiguration.delete().where(
                    SpawnerConfigurationXSimulationConfiguration.simulation_configuration
                    == simulation.id
                ).execute()
                SpawnerConfigurationXSimulationConfiguration.create(
                    simulation_configuration=simulation,
                    spawner_configuration=spawner_configuration,
                )

            # Remove and add references between simulation configuration and platform blocked fault
            check_and_update_configuration_references(
                simulation,
                platform_blocked_fault["key"],
                PlatformBlockedFaultConfigurationXSimulationConfiguration,
                platform_blocked_fault["column"],
                body,
            )

            # Remove and add references between simulation configuration and schedule blocked fault
            check_and_update_configuration_references(
                simulation,
                schedule_blocked_fault["key"],
                ScheduleBlockedFaultConfigurationXSimulationConfiguration,
                schedule_blocked_fault["column"],
                body,
            )

            # Remove and add references between simulation configuration and track blocked fault
            check_and_update_configuration_references(
                simulation,
                track_blocked_fault["key"],
                TrackBlockedFaultConfigurationXSimulationConfiguration,
                track_blocked_fault["column"],
                body,
            )

            # Remove and add references between simulation configuration and track speed limit fault
            check_and_update_configuration_references(
                simulation,
                track_speed_limit_fault["key"],
                TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
                track_speed_limit_fault["column"],
                body,
            )

            # Remove and add references between simulation configuration and train prio fault
            check_and_update_configuration_references(
                simulation,
                train_prio_fault["key"],
                TrainPrioFaultConfigurationXSimulationConfiguration,
                train_prio_fault["column"],
                body,
            )

            # Remove and add references between simulation configuration and train speed fault
            check_and_update_configuration_references(
                simulation,
                train_speed_fault["key"],
                TrainSpeedFaultConfigurationXSimulationConfiguration,
                train_speed_fault["column"],
                body,
            )

    except peewee.IntegrityError as error:
        print(error)
        return (
            {"error": "Configuration not found"},
            404,
        )

    return "Updated simulation configuration", 200


def delete_simulation_configuration(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["identifier"]
    :param token: Token object of the current user

    """
    simulation_configuration_id = options["identifier"]

    simulation_configurations = SimulationConfiguration.select().where(
        SimulationConfiguration.id == simulation_configuration_id
    )

    if not simulation_configurations.exists():
        return "Simulation not found", 404

    simulation_configuration = simulation_configurations.get()

    if simulation_configuration.runs.count() > 0:
        return "Simulation configuration is used in a run", 400

    with db.atomic():
        SpawnerConfigurationXSimulationConfiguration.delete().where(
            SpawnerConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()
        PlatformBlockedFaultConfigurationXSimulationConfiguration.delete().where(
            PlatformBlockedFaultConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()
        ScheduleBlockedFaultConfigurationXSimulationConfiguration.delete().where(
            ScheduleBlockedFaultConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()
        TrackBlockedFaultConfigurationXSimulationConfiguration.delete().where(
            TrackBlockedFaultConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()
        TrackSpeedLimitFaultConfigurationXSimulationConfiguration.delete().where(
            TrackSpeedLimitFaultConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()
        TrainPrioFaultConfigurationXSimulationConfiguration.delete().where(
            TrainPrioFaultConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()
        TrainSpeedFaultConfigurationXSimulationConfiguration.delete().where(
            TrainSpeedFaultConfigurationXSimulationConfiguration.simulation_configuration
            == simulation_configuration.id
        ).execute()

        simulation_configuration.delete_instance()
    return "Deleted simulation", 204


def check_and_create_configuration_references(
    simulation: SimulationConfiguration,
    key: str,
    table: BaseModel,
    column: str,
    body: any,
):
    """
    Create the references between the simulation configuration
    and the component configuration given the list of configuration ids.

    :param simulation: The simulation configuration
    :param key: The key of the list of configuration ids in the body
    :param table: The table to create the references in
    :param column: The column to create the references in
    :param body: The body of the request
    """
    if key in body:
        configuration_ids = body[key]
        create_configuration_references(simulation, table, configuration_ids, column)


def check_and_update_configuration_references(
    simulation: SimulationConfiguration,
    key: str,
    table: BaseModel,
    column: str,
    body: any,
):
    """
    Update the references between the simulation configuration and the component configuration
    if the list of configuration ids has changed.

    :param simulation: The simulation configuration
    :param key: The key of the list of configuration ids in the body
    :param table: The table to create the references in
    :param column: The column to create the references in
    :param body: The body of the request
    """
    if key in body:
        configuration_ids = body[key]
        table.delete().where(table.simulation_configuration == simulation.id).execute()
        create_configuration_references(simulation, table, configuration_ids, column)


def create_configuration_references(
    simulation: SimulationConfiguration,
    table: BaseModel,
    configuration_ids: list[str],
    column: str,
):
    """
    Create the references between the simulation configuration.

    :param simulation: The simulation configuration
    :param table: The table to create the references in
    :param configuration_ids: The list of configuration ids
    :param column: The column to create the references in
    """
    for configuration_id in configuration_ids:
        table.create(
            **{
                "simulation_configuration": simulation,
                column: configuration_id,
            }
        )
