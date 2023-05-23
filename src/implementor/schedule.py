# pylint: disable=unused-argument
# pylint: disable=duplicate-code
import os

import peewee

from src.base_model import db
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)

AVAILABLE_PLATFORMS = os.getenv("AVAILABLE_PLATFORMS", "").split(",")


def get_all_schedule_ids(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["strategy"]: Specify strategy of schedule
    :param token: Token object of the current user

    """
    strategy = options.get("strategy")

    # I disabled pylint because I'm really sure that it's an iterable
    # pylint: disable=not-an-iterable
    config_ids = [
        str(config.id)
        for config in ScheduleConfiguration.select().where(
            ScheduleConfiguration.strategy_type == strategy
        )
    ]
    # pylint: enable=not-an-iterable

    return config_ids, 200


def create_schedule(body, options, token):
    """

    :param body: The parsed body of the request
    :param options: A dictionary containing all the parameters for the Operations
        options["strategy"]: Specify strategy of schedule
    :param token: Token object of the current user
    """

    # Implement your business logic here
    # All the parameters are present in the options argument
    strategy = options.get("strategy")
    platforms = body.pop("platforms")

    try:
        with db.atomic():
            config = ScheduleConfiguration.create(
                strategy_type=strategy,
                **body,
            )
            for index, platform in enumerate(platforms):
                if platform not in AVAILABLE_PLATFORMS:
                    raise peewee.IntegrityError
                ScheduleConfigurationXSimulationPlatform.create(
                    schedule_configuration_id=config,
                    simulation_platform_id=platform,
                    index=index,
                )

        return {"id": str(config.id)}, 201
    except peewee.IntegrityError:
        return "Platform not found", 404


def get_schedule(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]: Specify id of schedule
        options["strategy"]: Specify strategy of schedule
    :param token: Token object of the current user

    """
    strategy = options.get("strategy")
    config_id = options.get("identifier")

    configs = ScheduleConfiguration.select().where(
        (ScheduleConfiguration.strategy_type == strategy)
        & (ScheduleConfiguration.id == config_id)
    )

    if not configs.exists():
        return "Schedule not found", 404

    config = configs.get()
    return config.to_dict(), 200


def delete_schedule(options, token):
    """
    :param options: A dictionary containing all the parameters for the Operations
        options["identifier"]: Specify id of schedule
        options["strategy"]: Specify strategy of schedule
    :param token: Token object of the current user

    """

    strategy = options.get("strategy")
    config_id = options.get("identifier")

    configs = ScheduleConfiguration.select().where(
        (ScheduleConfiguration.strategy_type == strategy)
        & (ScheduleConfiguration.id == config_id)
    )

    if not configs.exists():
        return "Schedule not found", 404

    config = configs.get()

    if config.spawner_configuration_references.exists():
        return (
            "Schedule configuration is referenced by a spawner configuration",
            400,
        )

    ScheduleConfigurationXSimulationPlatform.delete().where(
        ScheduleConfigurationXSimulationPlatform.schedule_configuration_id == config
    ).execute()
    config.delete_instance()
    return "Schedule deleted", 204
