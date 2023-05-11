# pylint: disable=unused-argument
# pylint: disable=duplicate-code
import json

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

    def check_and_create_configuration_references(
        simulation: SimulationConfiguration,
        key: str,
        table: BaseModel,
        column: str,
    ):
        """
        Create the references between the simulation configuration
        and the component configuration given the list of configuration ids.
        """
        if key in body:
            configuration_ids = body[key]
            for configuration_id in configuration_ids:
                table.create(
                    **{
                        "simulation_configuration": simulation,
                        column: configuration_id,
                    }
                )

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
            platform_blocked_fault = {
                "key": "platform_blocked_fault",
                "column": "platform_blocked_fault_configuration",
            }
            check_and_create_configuration_references(
                simulation,
                platform_blocked_fault["key"],
                PlatformBlockedFaultConfigurationXSimulationConfiguration,
                platform_blocked_fault["column"],
            )

            # Add references between simulation configuration and schedule blocked fault
            schedule_blocked_fault = {
                "key": "schedule_blocked_fault",
                "column": "schedule_blocked_fault_configuration",
            }
            check_and_create_configuration_references(
                simulation,
                schedule_blocked_fault["key"],
                ScheduleBlockedFaultConfigurationXSimulationConfiguration,
                schedule_blocked_fault["column"],
            )

            # Add references between simulation configuration and track blocked fault
            track_blocked_fault = {
                "key": "track_blocked_fault",
                "column": "track_blocked_fault_configuration",
            }
            check_and_create_configuration_references(
                simulation,
                track_blocked_fault["key"],
                TrackBlockedFaultConfigurationXSimulationConfiguration,
                track_blocked_fault["column"],
            )

            # Add references between simulation configuration and track speed limit fault
            track_speed_limit_fault = {
                "key": "track_speed_limit_fault",
                "column": "track_speed_limit_fault_configuration",
            }
            check_and_create_configuration_references(
                simulation,
                track_speed_limit_fault["key"],
                TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
                track_speed_limit_fault["column"],
            )

            # Add references between simulation configuration and train prio fault
            train_prio_fault = {
                "key": "train_prio_fault",
                "column": "train_prio_fault_configuration",
            }
            check_and_create_configuration_references(
                simulation,
                train_prio_fault["key"],
                TrainPrioFaultConfigurationXSimulationConfiguration,
                train_prio_fault["column"],
            )

            # Add references between simulation configuration and train speed fault
            train_speed_fault = {
                "key": "train_speed_fault",
                "column": "train_speed_fault_configuration",
            }
            check_and_create_configuration_references(
                simulation,
                train_speed_fault["key"],
                TrainSpeedFaultConfigurationXSimulationConfiguration,
                train_speed_fault["column"],
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
