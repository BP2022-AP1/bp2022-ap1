import hashlib

import pytest
from traci import vehicle

from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
    PlatformBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
    TrackBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
    TrainPrioFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
    TrainSpeedFaultConfigurationXSimulationConfiguration,
)
from src.implementor.models import Run, SimulationConfiguration, Token
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
)
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.schedule.train_schedule import TrainSchedule
from src.spawner.spawner import (
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
    SpawnerConfigurationXSimulationConfiguration,
)
from src.wrapper.simulation_objects import Edge, Platform, Track, Train


@pytest.fixture
def token():
    clear_token = "token"
    hashed_token = hashlib.sha256(clear_token.encode()).hexdigest()
    name = "user"
    permission = "user"
    return Token.create(name=name, permission=permission, hashedToken=hashed_token)


# ------------- InterlockingConfiguration ----------------
@pytest.fixture
def interlocking_configuration():
    return InterlockingConfiguration.create(dynamicRouting=True)


# ------------- ScheduleConfiguration ----------------


@pytest.fixture
def strategy_start_tick() -> int:
    return 1000


@pytest.fixture
def strategy_end_tick() -> int:
    return 2000


@pytest.fixture
def regular_strategy_frequency() -> int:
    return 100


@pytest.fixture
def regular_train_schedule_data(
    strategy_start_tick: int, strategy_end_tick: int, regular_strategy_frequency: int
) -> dict[str, any]:
    return {
        "schedule_type": "TrainSchedule",
        "strategy_type": "RegularScheduleStrategy",
        "strategy_start_tick": strategy_start_tick,
        "strategy_end_tick": strategy_end_tick,
        "train_schedule_train_type": "passenger",
        "regular_strategy_frequency": regular_strategy_frequency,
    }


@pytest.fixture
def platform_ids() -> list[str]:
    return [
        "399ec209-5f72-47be-a821-31a177021311",
        "2cf25596-24cf-49ee-ab44-323522bc2fc1",
        "ccffa906-9324-42bb-afed-a0f923f7e934",
        "f97dd0ba-5c3d-4a71-a1ac-01aca73aa8ce",
        "67e5c841-9fcd-47c3-b33f-d856c3c0b3f4",
        "5e47bb48-82ba-47ea-8295-c70c2c46cdba",
        "9ac02dac-6f0f-4779-b730-c2b22e1d8258",
        "91ce408a-5509-43f6-bb89-137feb0d14f2",
    ]


@pytest.fixture
def regular_train_schedule_configuration(
    regular_train_schedule_data: dict[str, any], platform_ids: list[str]
) -> RegularScheduleStrategy:
    configuration = ScheduleConfiguration(**regular_train_schedule_data)
    configuration.save()
    for index, platform_id in enumerate(platform_ids):
        ScheduleConfigurationXSimulationPlatform(
            schedule_configuration_id=configuration.id,
            simulation_platform_id=platform_id,
            index=index,
        ).save()
    return configuration


@pytest.fixture
def regular_train_schedule(
    regular_train_schedule_configuration: RegularScheduleStrategy,
) -> TrainSchedule:
    return TrainSchedule.from_schedule_configuration(
        regular_train_schedule_configuration
    )


# ------------- SpawnerConfiguration ----------------


@pytest.fixture
def spawner_configuration_data(
    regular_train_schedule: TrainSchedule,
) -> dict[str, any]:
    return {
        "schedule": [regular_train_schedule.id],
    }


@pytest.fixture
def spawner_configuration(
    spawner_configuration_data: dict[str, any],
) -> SpawnerConfiguration:
    configuration = SpawnerConfiguration()
    configuration.save()
    for schedule_configuration_id in spawner_configuration_data["schedule"]:
        SpawnerConfigurationXSchedule(
            spawner_configuration_id=configuration.id,
            schedule_configuration_id=schedule_configuration_id,
        ).save()
    return configuration


@pytest.fixture
def another_spawner_configuration(
    spawner_configuration_data: dict[str, any],
) -> SpawnerConfiguration:
    configuration = SpawnerConfiguration()
    configuration.save()
    for schedule_configuration_id in spawner_configuration_data["schedule"]:
        SpawnerConfigurationXSchedule(
            spawner_configuration_id=configuration.id,
            schedule_configuration_id=schedule_configuration_id,
        ).save()
    return configuration


# ------------- PlatformBlockedFaultConfiguration ----------------


@pytest.fixture
def platform() -> Platform:
    return Platform("fault injector platform")


@pytest.fixture
def platform_blocked_fault_configuration_data(platform: Platform) -> dict:
    return {
        "start_tick": 20,
        "end_tick": 200,
        "description": "test PlatformBlockedFault",
        "affected_element_id": platform.identifier,
        "strategy": "regular",
    }


@pytest.fixture
def platform_blocked_fault_configuration(
    platform_blocked_fault_configuration_data,
) -> PlatformBlockedFaultConfiguration:
    return PlatformBlockedFaultConfiguration.create(
        **platform_blocked_fault_configuration_data
    )


@pytest.fixture
def another_platform_blocked_fault_configuration(
    platform_blocked_fault_configuration_data,
) -> PlatformBlockedFaultConfiguration:
    return PlatformBlockedFaultConfiguration.create(
        **platform_blocked_fault_configuration_data
    )


# ------------- TrackBlockedFaultConfiguration ----------------


@pytest.fixture
def edge() -> Edge:
    return Edge("fault injector track")


@pytest.fixture
def edge_re() -> Edge:
    return Edge("fault injector track-re")


@pytest.fixture
def track(edge, edge_re):
    return Track(edge, edge_re)


@pytest.fixture
def track_blocked_fault_configuration_data(track: Track) -> dict:
    return {
        "start_tick": 30,
        "end_tick": 300,
        "description": "test TrackBlockedFault",
        "affected_element_id": track.identifier,
        "strategy": "regular",
    }


@pytest.fixture
def track_blocked_fault_configuration(track_blocked_fault_configuration_data):
    return TrackBlockedFaultConfiguration.create(
        **track_blocked_fault_configuration_data
    )


@pytest.fixture
def another_track_blocked_fault_configuration(
    track_blocked_fault_configuration_data,
):
    return TrackBlockedFaultConfiguration.create(
        **track_blocked_fault_configuration_data
    )


# ------------- TrackSpeedLimitFaultConfiguration ----------------


@pytest.fixture
def track_speed_limit_fault_configuration_data(
    track: Track,
) -> dict:
    return {
        "start_tick": 4,
        "end_tick": 130,
        "description": "test TrackSpeedLimitFault",
        "affected_element_id": track.identifier,
        "new_speed_limit": 60,
        "strategy": "regular",
    }


@pytest.fixture
def track_speed_limit_fault_configuration(
    track_speed_limit_fault_configuration_data: dict,
) -> TrackSpeedLimitFaultConfiguration:
    return TrackSpeedLimitFaultConfiguration.create(
        **track_speed_limit_fault_configuration_data
    )


@pytest.fixture
def another_track_speed_limit_fault_configuration(
    track_speed_limit_fault_configuration_data: dict,
) -> TrackSpeedLimitFaultConfiguration:
    return TrackSpeedLimitFaultConfiguration.create(
        **track_speed_limit_fault_configuration_data
    )


# ------------- TrainPrioFaultConfiguration ----------------


@pytest.fixture
def train_prio_fault_configuration_data(basic_train: Train) -> dict:
    return {
        "start_tick": 50,
        "end_tick": 500,
        "description": "test TrainPrioFault",
        "affected_element_id": basic_train.identifier,
        "new_prio": 3,
        "strategy": "regular",
    }


@pytest.fixture
def train_prio_fault_configuration(train_prio_fault_configuration_data):
    return TrainPrioFaultConfiguration.create(**train_prio_fault_configuration_data)


@pytest.fixture
def another_train_prio_fault_configuration(
    train_prio_fault_configuration_data,
):
    return TrainPrioFaultConfiguration.create(**train_prio_fault_configuration_data)


# ------------- TrainSpeedLimitFaultConfiguration ----------------


@pytest.fixture
def train_speed_fault_configuration(
    basic_train: Train,
) -> TrainSpeedFaultConfiguration:
    return TrainSpeedFaultConfiguration.create(
        start_tick=40,
        end_tick=400,
        description="test TrainSpeedFault",
        affected_element_id=basic_train.identifier,
        new_speed=30,
        strategy="regular",
    )


# ------------- TrainSpeedFaultConfiguration ----------------


@pytest.fixture
def train_speed_fault_configuration_data(basic_train: Train) -> dict:
    return {
        "start_tick": 40,
        "end_tick": 400,
        "description": "test TrainSpeedFault",
        "affected_element_id": basic_train.identifier,
        "new_speed": 30,
        "strategy": "regular",
    }


@pytest.fixture
def train_speed_fault_configuration(train_speed_fault_configuration_data):
    return TrainSpeedFaultConfiguration.create(**train_speed_fault_configuration_data)


@pytest.fixture
def another_train_speed_fault_configuration(
    train_speed_fault_configuration_data,
):
    return TrainSpeedFaultConfiguration.create(**train_speed_fault_configuration_data)


# ------------- ScheduleBlockedFaultConfiguration ----------------


@pytest.fixture
def schedule():
    schedule_configuration = ScheduleConfiguration(
        schedule_type="TrainSchedule",
        strategy_type="RegularScheduleStrategy",
        train_schedule_train_type="cargo",
        regular_strategy_start_tick=10,
        regular_strategy_frequency=100,
    )
    schedule_configuration.save()
    return schedule_configuration


@pytest.fixture
def schedule_blocked_fault_configuration_data(schedule) -> dict:
    return {
        "start_tick": 30,
        "end_tick": 300,
        "description": "test ScheduleBlockedFault",
        "affected_element_id": schedule.id,
        "strategy": "regular",
    }


@pytest.fixture
def schedule_blocked_fault_configuration(
    schedule_blocked_fault_configuration_data: dict,
) -> ScheduleBlockedFaultConfiguration:
    return ScheduleBlockedFaultConfiguration.create(
        **schedule_blocked_fault_configuration_data
    )


@pytest.fixture
def another_schedule_blocked_fault_configuration(
    schedule_blocked_fault_configuration_data: dict,
) -> ScheduleBlockedFaultConfiguration:
    return ScheduleBlockedFaultConfiguration.create(
        **schedule_blocked_fault_configuration_data
    )


# ------------- SimulationConfiguration ----------------


@pytest.fixture
def simulation_configuration_data(
    spawner_configuration,
    platform_blocked_fault_configuration,
    schedule_blocked_fault_configuration,
    track_blocked_fault_configuration,
    track_speed_limit_fault_configuration,
    train_prio_fault_configuration,
    train_speed_fault_configuration,
):
    return {
        "spawner": spawner_configuration.id,
        "platform_blocked_fault": [platform_blocked_fault_configuration.id],
        "schedule_blocked_fault": [schedule_blocked_fault_configuration.id],
        "track_blocked_fault": [track_blocked_fault_configuration.id],
        "track_speed_limit_fault": [track_speed_limit_fault_configuration.id],
        "train_prio_fault": [train_prio_fault_configuration.id],
        "train_speed_fault": [train_speed_fault_configuration.id],
    }


@pytest.fixture
def simulation_configuration_full(
    spawner_configuration,
    platform_blocked_fault_configuration,
    schedule_blocked_fault_configuration,
    track_blocked_fault_configuration,
    track_speed_limit_fault_configuration,
    train_prio_fault_configuration,
    train_speed_fault_configuration,
):
    configuration = SimulationConfiguration()
    configuration.save()

    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        spawner_configuration=spawner_configuration,
    )
    PlatformBlockedFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        platform_blocked_fault_configuration=platform_blocked_fault_configuration,
    )
    ScheduleBlockedFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        schedule_blocked_fault_configuration=schedule_blocked_fault_configuration,
    )
    TrackBlockedFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        track_blocked_fault_configuration=track_blocked_fault_configuration,
    )
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        track_speed_limit_fault_configuration=track_speed_limit_fault_configuration,
    )
    TrainSpeedFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        train_speed_fault_configuration=train_speed_fault_configuration,
    )
    TrainPrioFaultConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        train_prio_fault_configuration=train_prio_fault_configuration,
    )

    return configuration


@pytest.fixture
def empty_simulation_configuration_data(spawner_configuration):
    return {"spawner": spawner_configuration.id}


@pytest.fixture
def empty_simulation_configuration(empty_simulation_configuration_data):
    configuration = SimulationConfiguration()
    configuration.save()
    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        spawner_configuration=empty_simulation_configuration_data["spawner"],
    )
    return configuration


@pytest.fixture
def another_empty_simulation_configuration(empty_simulation_configuration_data):
    configuration = SimulationConfiguration()
    configuration.save()
    SpawnerConfigurationXSimulationConfiguration.create(
        simulation_configuration=configuration,
        spawner_configuration=empty_simulation_configuration_data["spawner"],
    )
    return configuration
