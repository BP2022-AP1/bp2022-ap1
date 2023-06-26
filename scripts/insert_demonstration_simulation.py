from datetime import datetime

from src.base_model import db
from src.implementor.models import SimulationConfiguration
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)

with db.atomic():
    platforms = ["bs_0", "bs_1"]
    regular_schedule = ScheduleConfiguration.create(
        schedule_type="TrainSchedule",
        strategy_type="RegularScheduleStrategy",
        strategy_start_time=0,
        strategy_end_time=7200,
        train_schedule_train_type="regio",
        regular_strategy_frequency=180,
    )
    platforms2 = ["bs_2", "bs_3"]

    random_schedule = ScheduleConfiguration.create(
        schedule_type="TrainSchedule",
        strategy_type="RandomScheduleStrategy",
        strategy_start_time=0,
        strategy_end_time=7200,
        random_strategy_trains_per_1000_seconds=2.0,
    )
    print(f"regular schedule: {regular_schedule.id}")
    print(f"radom schedule: {random_schedule.id}")
    for index, platform in enumerate(platforms):
        ScheduleConfigurationXSimulationPlatform.create(
            schedule_configuration_id=regular_schedule,
            simulation_platform_id=platform,
            index=index,
        )

    for index, platform in enumerate(platforms2):
        ScheduleConfigurationXSimulationPlatform.create(
            schedule_configuration_id=random_schedule,
            simulation_platform_id=platform,
            index=index,
        )

    spawner_configuration = SpawnerConfiguration()
    spawner_configuration.save()
    print(f"schedule configuration: {spawner_configuration.id}")

    SpawnerConfigurationXSchedule(
        spawner_configuration_id=spawner_configuration,
        schedule_configuration_id=regular_schedule,
    ).save()

    SpawnerConfigurationXSchedule(
        spawner_configuration_id=spawner_configuration,
        schedule_configuration_id=random_schedule,
    ).save()

    simulation_configuration = SimulationConfiguration.create()
    print(f"simulation configuration: {simulation_configuration.id}")

    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration,
        spawner_configuration=spawner_configuration,
    )