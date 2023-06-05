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
    platforms = ["bs_0", "bs_3"]
    regular_schedule = ScheduleConfiguration.create(
        schedule_type="TrainSchedule",
        strategy_type="RegularScheduleStrategy",
        strategy_start_tick=100,
        strategy_end_tick=20000,
        train_schedule_train_type="regio",
        regular_strategy_frequency=3000,
    )
    print(f"regular schedule: {regular_schedule.id}")
    for index, platform in enumerate(platforms):
        ScheduleConfigurationXSimulationPlatform.create(
            schedule_configuration_id=regular_schedule,
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

    simulation_configuration = SimulationConfiguration.create()
    print(f"simulation configuration: {simulation_configuration.id}")

    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration,
        spawner_configuration=spawner_configuration,
    )
