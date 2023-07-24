from datetime import datetime

from src.base_model import db
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)
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
        strategy_end_time=24 * 60 * 60,  # 24h
        train_schedule_train_type="regio",
        regular_strategy_frequency=180,
    )
    platforms2 = ["bs_2", "bs_3"]
    demand_schedule = ScheduleConfiguration.create(
        schedule_type="TrainSchedule",
        strategy_type="DemandScheduleStrategy",
        strategy_start_time=0,
        strategy_end_time=24 * 60 * 60,  # 24h
        train_schedule_train_type="cargo",
        demand_strategy_power_station="schwarze_pumpe",
        demand_strategy_scaling_factor=1.0,
        demand_strategy_start_datetime=datetime(2020, 1, 1, 0, 0, 0),
    )
    print(f"regular schedule: {regular_schedule.id}")
    print(f"demand schedule: {demand_schedule.id}")
    for index, platform in enumerate(platforms):
        ScheduleConfigurationXSimulationPlatform.create(
            schedule_configuration_id=regular_schedule,
            simulation_platform_id=platform,
            index=index,
        )

    for index, platform in enumerate(platforms2):
        ScheduleConfigurationXSimulationPlatform.create(
            schedule_configuration_id=demand_schedule,
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
        schedule_configuration_id=demand_schedule,
    ).save()

    simulation_configuration = SimulationConfiguration.create()
    print(f"simulation configuration: {simulation_configuration.id}")

    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration,
        spawner_configuration=spawner_configuration,
    )

    schedule_blocked_fault_configuration = ScheduleBlockedFaultConfiguration.create(
        start_time=2000,
        end_time=3500,
        description="test ScheduleBlockedFault",
        affected_element_id=regular_schedule.id,
        strategy="regular",
    )
    ScheduleBlockedFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration,
        schedule_blocked_fault_configuration=schedule_blocked_fault_configuration,
    )