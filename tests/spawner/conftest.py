import pytest

from src.implementor.models import SimulationConfiguration, Token
from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.schedule.train_schedule import TrainSchedule
from src.spawner.spawner import (
    Spawner,
    SpawnerConfiguration,
    SpawnerConfigurationXSchedule,
)
from src.wrapper.simulation_objects import Train


@pytest.fixture
def strategy_start_tick() -> int:
    return 1000


@pytest.fixture
def strategy_end_tick() -> int:
    return 10000


@pytest.fixture
def regular_strategy_frequency() -> int:
    return 100


@pytest.fixture
def random_strategy_trains_per_1000_ticks() -> float:
    return 10.0


@pytest.fixture
def random_strategy_seed() -> int:
    return 42


@pytest.fixture
def random_strategy_spawn_ticks() -> list[int]:
    # These are the ticks at which trains are spawned when using seed=42
    # and trains_per_1000_ticks=10.0
    return [
        1019,
        1124,
        1269,
        1290,
        1297,
        1368,
        1394,
        1427,
        1481,
        1684,
        1882,
        2026,
        2133,
        2168,
        2174,
        2391,
        2807,
        2836,
        2961,
        3112,
        3120,
        3153,
        3221,
        3426,
        3516,
        3543,
        3563,
        3568,
        3587,
        3735,
        3748,
        3755,
        3924,
        3990,
        4207,
        4211,
        4313,
        4406,
        4517,
        4712,
        4739,
        4801,
        4844,
        5033,
        5071,
        5101,
        5152,
        5350,
        5355,
        5359,
        5363,
        5451,
        5497,
        5730,
        5937,
        6009,
        6027,
        6102,
        6228,
        6245,
        6500,
        6602,
        6624,
        6715,
        6879,
        6967,
        7634,
        7735,
        7779,
        7914,
        7938,
        8174,
        8179,
        8215,
        8238,
        8302,
        8391,
        8418,
        8557,
        8590,
        8655,
        8749,
        8857,
        8982,
        9017,
        9022,
        9140,
        9219,
        9308,
        9370,
        9398,
        9495,
        9703,
        9838,
        9877,
        9983,
    ]


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
def random_train_schedule_data(
    strategy_start_tick: int,
    strategy_end_tick: int,
    random_strategy_trains_per_1000_ticks: float,
    random_strategy_seed: int,
) -> dict[str, any]:
    return {
        "schedule_type": "TrainSchedule",
        "strategy_type": "RandomScheduleStrategy",
        "strategy_start_tick": strategy_start_tick,
        "strategy_end_tick": strategy_end_tick,
        "train_schedule_train_type": "cargo",
        "random_strategy_trains_per_1000_ticks": random_strategy_trains_per_1000_ticks,
        "random_strategy_seed": random_strategy_seed,
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
    configuration = ScheduleConfiguration.from_dict(regular_train_schedule_data)
    configuration.save()
    for index, platform_id in enumerate(platform_ids):
        ScheduleConfigurationXSimulationPlatform(
            schedule_configuration_id=configuration.id,
            simulation_platform_id=platform_id,
            index=index,
        ).save()
    return configuration


@pytest.fixture
def random_train_schedule_configuration(
    random_train_schedule_data: dict[str, any], platform_ids: list[str]
) -> RandomScheduleStrategy:
    configuration = ScheduleConfiguration.from_dict(random_train_schedule_data)
    configuration.save()
    for index, platform_id in enumerate(platform_ids):
        ScheduleConfigurationXSimulationPlatform(
            schedule_configuration_id=configuration.id,
            simulation_platform_id=platform_id,
            index=index,
        ).save()
    return configuration


@pytest.fixture
def regular_strategy(
    regular_train_schedule_configuration: RegularScheduleStrategy,
) -> RegularScheduleStrategy:
    return RegularScheduleStrategy.from_schedule_configuration(
        regular_train_schedule_configuration
    )


@pytest.fixture
def random_strategy(
    random_train_schedule_configuration: RandomScheduleStrategy,
) -> RandomScheduleStrategy:
    return RandomScheduleStrategy.from_schedule_configuration(
        random_train_schedule_configuration
    )


@pytest.fixture
def regular_train_schedule(
    regular_train_schedule_configuration: RegularScheduleStrategy,
) -> TrainSchedule:
    return TrainSchedule.from_schedule_configuration(
        regular_train_schedule_configuration
    )


@pytest.fixture
def random_train_schedule(
    random_train_schedule_configuration: RandomScheduleStrategy,
) -> TrainSchedule:
    return TrainSchedule.from_schedule_configuration(
        random_train_schedule_configuration
    )


@pytest.fixture
def spawner_configuration(
    regular_train_schedule: TrainSchedule, random_train_schedule: TrainSchedule
) -> SpawnerConfiguration:
    configuration = SpawnerConfiguration()
    configuration.save()
    SpawnerConfigurationXSchedule(
        spawner_configuration_id=configuration.id,
        schedule_configuration_id=regular_train_schedule.id,
    ).save()
    SpawnerConfigurationXSchedule(
        spawner_configuration_id=configuration.id,
        schedule_configuration_id=random_train_schedule.id,
    ).save()
    return configuration


@pytest.fixture
def mock_logger() -> object:
    class MockLogger:
        """Mocks the logger."""

    return MockLogger()


@pytest.fixture
def mock_traci_wrapper() -> object:
    class MockTraciWrapper:
        """Mocks the TraCiWrapper."""

        train: Train

        def spawn_train(self, train: Train):
            self.train = train

    return MockTraciWrapper()


@pytest.fixture
def spawner(
    spawner_configuration: SpawnerConfiguration,
    mock_logger: object,
    mock_traci_wrapper: object,
) -> Spawner:
    return Spawner(
        configuration=spawner_configuration,
        logger=mock_logger,
        traci_wrapper=mock_traci_wrapper,
    )


@pytest.fixture
def token() -> Token:
    token = Token(name="owner", permission="admin", hashedToken="hash")
    token.save()
    return token


@pytest.fixture
def simulation_configuration(token) -> SimulationConfiguration:
    config = SimulationConfiguration(token=token)
    config.save()
    return config
