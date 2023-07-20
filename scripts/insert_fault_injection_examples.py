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

from src.fault_injector.fault_configurations.train_speed_fault_configuration import TrainSpeedFaultConfigurationXSimulationConfiguration, TrainSpeedFaultConfiguration
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import TrackSpeedLimitFaultConfiguration, TrackSpeedLimitFaultConfigurationXSimulationConfiguration
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import TrackBlockedFaultConfiguration, TrackBlockedFaultConfigurationXSimulationConfiguration
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import ScheduleBlockedFaultConfiguration, ScheduleBlockedFaultConfigurationXSimulationConfiguration

with db.atomic():
    platforms = ["bs_0", "bs_1"]

    # --- different schedules to try out the fault injection --- #
    regular_schedule = ScheduleConfiguration.create(
        schedule_type="TrainSchedule",
        strategy_type="RegularScheduleStrategy",
        strategy_start_time=0,
        strategy_end_time=7200,
        train_schedule_train_type="regio",
        regular_strategy_frequency=180,
        regular_strategy_frequency=400,
    )
    platforms2 = ["bs_2", "bs_3"]

    random_schedule = ScheduleConfiguration.create(
        schedule_type="TrainSchedule",
        strategy_type="RandomScheduleStrategy",
        strategy_start_time=0,
        strategy_end_time=7200,
        random_strategy_trains_per_1000_seconds=2.0,
    )
    # demand_schedule = ScheduleConfiguration.create(
    #     schedule_type="TrainSchedule",
    #     strategy_type="DemandScheduleStrategy",
    #     strategy_start_time=0,
    #     strategy_end_time=7200,
    #     train_schedule_train_type="cargo",
    #     demand_strategy_power_station="schwarze_pumpe",
    #     demand_strategy_scaling_factor=1.0,
    #     demand_strategy_start_datetime=datetime(2020, 1, 1, 0, 0, 0),
    # )
    print(f"regular schedule: {regular_schedule.id}")
    print(f"random schedule: {random_schedule.id}")
    # print(f"demand schedule: {demand_schedule.id}")
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
    # for index, platform in enumerate(platforms2):
    #     ScheduleConfigurationXSimulationPlatform.create(
    #         schedule_configuration_id=demand_schedule,
    #         simulation_platform_id=platform,
    #         index=index,
    #     )

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
    # SpawnerConfigurationXSchedule(
    #     spawner_configuration_id=spawner_configuration,
    #     schedule_configuration_id=demand_schedule,
    # ).save()

    simulation_configuration = SimulationConfiguration.create()
    print(f"simulation configuration: {simulation_configuration.id}")
    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration,
        spawner_configuration=spawner_configuration,
    )

    #############################################################################
    # --- different fault types, comment in and out or change what you want --- #
    #############################################################################

    # train_speed_fault_configuration = TrainSpeedFaultConfiguration.create(
    #             affected_element_id=str(regular_schedule.id) + "_8000_regio",
    #             new_speed=15,
    #             start_time=1000,
    #             end_time=700,
    #             description="test TrainSpeedFault",
    #             strategy="regular",
    # )
    # TrainSpeedFaultConfigurationXSimulationConfiguration.create(
    #     simulation_configuration=simulation_configuration, train_speed_fault_configuration=train_speed_fault_configuration
    # )

    # track_speed_limit_fault_configuration = TrackSpeedLimitFaultConfiguration.create(
    #             affected_element_id="c6894-2-re",
    #             new_speed_limit=10,
    #             start_time=200,
    #             end_time=3000,
    #             description="test TrackSpeedLimitFault",
    #             strategy="regular",
    # )
    # TrackSpeedLimitFaultConfigurationXSimulationConfiguration.create(
    #     simulation_configuration=simulation_configuration, track_speed_limit_fault_configuration=track_speed_limit_fault_configuration
    # )


    # track_blocked_fault_configuration_1 = TrackBlockedFaultConfiguration.create(
    #             affected_element_id="b8f37-2-re",
    #             start_time=200,
    #             end_time=3000,
    #             description="test TrackBlockedFault",
    #             strategy="regular",
    # ) 
    # TrackBlockedFaultConfigurationXSimulationConfiguration.create(
    #     simulation_configuration=simulation_configuration, track_blocked_fault_configuration=track_blocked_fault_configuration_1
    # )

    track_blocked_fault_configuration_2 = TrackBlockedFaultConfiguration.create(
                affected_element_id="d5792-0-re",
                start_time=200,
                end_time=3000,
                description="test TrackBlockedFault",
                strategy="regular",
    )
    TrackBlockedFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=simulation_configuration, track_blocked_fault_configuration=track_blocked_fault_configuration_2
    )

    # schedule_blocked_fault_configuration = ScheduleBlockedFaultConfiguration.create(
    #             start_time=600,
    #             end_time=950,
    #             description="test ScheduleBlockedFault",
    #             affected_element_id=regular_schedule.id,
    #             strategy="regular",
    # )
    # ScheduleBlockedFaultConfigurationXSimulationConfiguration.create(
    #     simulation_configuration=simulation_configuration, schedule_blocked_fault_configuration=schedule_blocked_fault_configuration
    # )