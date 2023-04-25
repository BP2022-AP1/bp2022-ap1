import json
import os
from datetime import datetime

import pytest

from src.schedule.demand_schedule_strategy import DemandScheduleStrategy
from src.schedule.random_schedule_strategy import RandomScheduleStrategy
from src.schedule.regular_schedule_strategy import RegularScheduleStrategy
from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
from src.schedule.smard_api import SmardApi
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
def demand_strategy_spawn_ticks() -> list[int]:
    return [
        1900,
        2800,
        3700,
        4600,
        5500,
        7300,
        8200,
        9100,
        10000,
        10900,
        11800,
        13600,
        14500,
        15400,
        16300,
        17200,
        18100,
        19000,
        20800,
        21700,
        22600,
        23500,
        24400,
        25300,
        26200,
        28000,
        28900,
        29800,
        30700,
        31600,
        32500,
        33400,
        35200,
        36100,
        37000,
        37900,
        38800,
        39700,
        40600,
        42400,
        43300,
        44200,
        45100,
        46000,
        46900,
        47800,
        48700,
        50500,
        51400,
        52300,
        53200,
        54100,
        55000,
        55900,
        57700,
        58600,
        59500,
        60400,
        61300,
        62200,
        63100,
        64900,
        65800,
        66700,
        67600,
        68500,
        69400,
        70300,
        71200,
        73000,
        73900,
        74800,
        75700,
        76600,
        77500,
        78400,
        79300,
        80200,
        81100,
        82000,
        83800,
        84700,
        85600,
        86500,
        88300,
        89200,
        91000,
        92800,
        93700,
        95500,
        97300,
        98200,
        100000,
        101800,
        102700,
        104500,
        106300,
        107200,
        109000,
        110800,
        111700,
        112600,
        114400,
        115300,
        117100,
        118000,
        119800,
        121600,
        122500,
        124300,
        125200,
        127000,
        127900,
        129700,
        130600,
        132400,
        134200,
        135100,
        136900,
        137800,
        139600,
        140500,
        142300,
        143200,
        145000,
        145900,
        146800,
        148600,
        149500,
        150400,
        151300,
        153100,
        154000,
        154900,
        155800,
        157600,
        158500,
        159400,
        160300,
        162100,
        163000,
        163900,
        164800,
        165700,
        167500,
        168400,
        169300,
        170200,
        171100,
        172000,
        172900,
        173800,
        175600,
        176500,
        177400,
        178300,
        179200,
        181000,
        181900,
        182800,
        183700,
        184600,
        186400,
        187300,
        188200,
        189100,
        190000,
        190900,
        191800,
        193600,
        194500,
        195400,
        196300,
        197200,
        198100,
        199000,
        200800,
        201700,
        202600,
        203500,
        204400,
        205300,
        206200,
        208000,
        208900,
        209800,
        210700,
        211600,
        212500,
        213400,
        214300,
        216100,
        217000,
        217900,
        218800,
        219700,
        220600,
        221500,
        222400,
        224200,
        225100,
        226000,
        226900,
        227800,
        228700,
        230500,
        231400,
        232300,
        233200,
        234100,
        235000,
        235900,
        237700,
        238600,
        239500,
        240400,
        241300,
        242200,
        243100,
        244900,
        245800,
        246700,
        247600,
        248500,
        249400,
        251200,
        252100,
        253000,
        253900,
        254800,
        255700,
        257500,
        258400,
        259300,
        260200,
        261100,
        262900,
        263800,
        264700,
        265600,
        266500,
        268300,
        269200,
        270100,
        271000,
        271900,
        273700,
        274600,
        275500,
        276400,
        277300,
        279100,
        280000,
        280900,
        281800,
        282700,
        284500,
        285400,
        286300,
        287200,
        288100,
        289000,
        290800,
        291700,
        292600,
        293500,
        294400,
        296200,
        297100,
        298000,
        298900,
        299800,
        301600,
        302500,
        303400,
        304300,
        305200,
        307000,
        307900,
        308800,
        309700,
        311500,
        312400,
        313300,
        314200,
        316000,
        316900,
        317800,
        318700,
        319600,
        321400,
        322300,
        323200,
        324100,
        325000,
        326800,
        327700,
        328600,
        329500,
        330400,
        331300,
        333100,
        334000,
        334900,
        335800,
        336700,
        338500,
        339400,
        340300,
        341200,
        342100,
        343900,
        344800,
        345700,
        346600,
        348400,
        349300,
        351100,
        352900,
        353800,
        355600,
        356500,
        358300,
        360100,
        361000,
        362800,
        364600,
        365500,
        366400,
        368200,
        369100,
        370000,
        370900,
        372700,
        373600,
        374500,
        375400,
        376300,
        378100,
        379000,
        379900,
        380800,
        381700,
        383500,
        384400,
        385300,
        386200,
        388000,
        388900,
        389800,
        390700,
        392500,
        393400,
        394300,
        395200,
        397000,
        397900,
        398800,
        399700,
        401500,
        402400,
        403300,
        404200,
        406000,
        406900,
        407800,
        408700,
        409600,
        410500,
        412300,
        413200,
        414100,
        415000,
        416800,
        417700,
        418600,
        419500,
        420400,
        422200,
        423100,
        424900,
        425800,
        427600,
        428500,
        430300,
        432100,
        433900,
        435700,
        438400,
        440200,
        442000,
        443800,
        445600,
        447400,
        449200,
        451900,
        453700,
        455500,
        457300,
        459100,
        460900,
        462700,
        464500,
        466300,
        467200,
        469000,
        470800,
        472600,
        474400,
        475300,
        477100,
        478000,
        479800,
        481600,
        482500,
        484300,
        486100,
        487900,
        489700,
        491500,
        492400,
        494200,
        496000,
        496900,
        498700,
        500500,
        501400,
        503200,
        505000,
        505900,
        507700,
        509500,
        511300,
        512200,
        514000,
        515800,
        517600,
        519400,
        521200,
        523900,
        526600,
        529300,
        531100,
        533800,
        536500,
        539200,
        541900,
        544600,
        547300,
        549100,
        551800,
        554500,
        557200,
        559900,
        562600,
        565300,
        568000,
        569800,
        572500,
        575200,
        577900,
        580600,
        582400,
        585100,
        586900,
        589600,
        591400,
        594100,
        596800,
        598600,
        601300,
        604000,
    ]


@pytest.fixture
def demand_strategy_power_station() -> str:
    return "boxberg"


@pytest.fixture
def demand_strategy_scaling_factor() -> float:
    return 1.0


@pytest.fixture
def demand_strategy_available_interval() -> tuple[datetime, datetime]:
    # an interval where data is available
    return (
        datetime.fromtimestamp(1420412400),
        datetime.fromtimestamp(1421622000),
    )


@pytest.fixture
def demand_strategy_not_available_past_interval() -> tuple[datetime, datetime]:
    # an interval where no data is available and the interval lies before
    # any other interval where data is available
    return (
        datetime.fromtimestamp(1417807500),
        datetime.fromtimestamp(1419807500),
    )


@pytest.fixture
def demand_strategy_not_available_future_interval() -> tuple[datetime, datetime]:
    # an interval where no data is available and the interval lies after
    # any other interval where data is available
    return (
        datetime.fromtimestamp(1981682400),
        datetime.fromtimestamp(2081682400),
    )


@pytest.fixture
def demand_strategy_start_not_available_interval() -> datetime:
    # an interval where data is available but some is
    # missing at the start of the interval
    return (
        datetime.fromtimestamp(1417807500),
        datetime.fromtimestamp(1420412400),
    )


@pytest.fixture
def demand_strategy_end_not_available_interval() -> datetime:
    # an interval where data is available but some is
    # missing at the end of the interval
    return (
        datetime.fromtimestamp(1424646000),
        datetime.fromtimestamp(2081682400),
    )


@pytest.fixture
def demand_strategy_all_none_interval() -> tuple[datetime, datetime]:
    # an interval where data is available but all values are None
    return (
        datetime.fromtimestamp(1419807600),
        datetime.fromtimestamp(1419878700),
    )


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
def demand_train_schedule_data(
    strategy_start_tick: int,
    demand_strategy_power_station: str,
    demand_strategy_scaling_factor: float,
    demand_strategy_available_interval: tuple[datetime, datetime],
) -> dict[str, any]:
    ticks = (
        demand_strategy_available_interval[1] - demand_strategy_available_interval[0]
    ).total_seconds()
    return {
        "schedule_type": "TrainSchedule",
        "strategy_type": "DemandScheduleStrategy",
        "strategy_start_tick": strategy_start_tick,
        "strategy_end_tick": strategy_start_tick + ticks,
        "train_schedule_train_type": "cargo",
        "demand_strategy_power_station": demand_strategy_power_station,
        "demand_strategy_scaling_factor": demand_strategy_scaling_factor,
        "demand_strategy_start_datetime": demand_strategy_available_interval[
            0
        ].isoformat(),
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
def demand_train_schedule_configuration(
    demand_train_schedule_data: dict[str, any], platform_ids: list[str]
) -> DemandScheduleStrategy:
    configuration = ScheduleConfiguration.from_dict(demand_train_schedule_data)
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
def monkeypatched_smard_api(monkeypatch) -> object:
    data_directory = "data/spawner/mock_smard_api_data"

    def _request_patch(_: object, url: str) -> dict:
        if "index" in url:
            filename = os.path.join(data_directory, "index.json")
        else:
            timestamp = url.split("_")[-1].split(".")[0]
            filename = os.path.join(data_directory, f"data_{timestamp}.json")
        with open(filename, "r") as file:
            return json.load(file)

    monkeypatch.setattr(SmardApi, "_request", _request_patch)
    return SmardApi()


@pytest.fixture
def demand_strategy(
    monkeypatch,
    demand_train_schedule_configuration: DemandScheduleStrategy,
    monkeypatched_smard_api: object,
) -> DemandScheduleStrategy:
    strategy = DemandScheduleStrategy.from_schedule_configuration(
        demand_train_schedule_configuration
    )
    monkeypatch.setattr(strategy, "_api", monkeypatched_smard_api)
    return strategy


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
def demand_train_schedule(
    demand_train_schedule_configuration: DemandScheduleStrategy,
) -> TrainSchedule:
    return TrainSchedule.from_schedule_configuration(
        demand_train_schedule_configuration
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
def mock_train_spawner() -> object:
    class MockTrainSpawner:
        """Mocks the TrainSpawner."""

        identifier: str
        timetable: list[str]
        train_type: str
        spawn_history: list[int]
        _next_spawn_fails: bool

        def __init__(self):
            self._next_spawn_fails = False
            self.spawn_history = []

        def spawn_train(
            self, identifier: str, timetable: list[str], train_type: str
        ) -> bool:
            if self._next_spawn_fails:
                self._next_spawn_fails = False
                return False
            self.spawn_history.append(int(identifier.split("_")[-1]))
            self.identifier = identifier
            self.timetable = timetable
            self.train_type = train_type
            return True

        def let_next_spawn_fail(self):
            self._next_spawn_fails = True

    return MockTrainSpawner()


@pytest.fixture
def spawner(
    spawner_configuration: SpawnerConfiguration,
    mock_logger: object,
    mock_train_spawner: object,
) -> Spawner:
    return Spawner(
        configuration=spawner_configuration,
        logger=mock_logger,
        train_spawner=mock_train_spawner,
    )
