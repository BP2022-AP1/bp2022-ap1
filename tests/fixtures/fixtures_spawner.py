import json
import os
from datetime import datetime

import pytest

from src.event_bus.event_bus import EventBus
from src.implementor.models import SimulationConfiguration, Token
from src.logger.logger import Logger
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


@pytest.fixture
def strategy_start_time() -> int:
    return 1000


@pytest.fixture
def strategy_end_time() -> int:
    return 2000


@pytest.fixture
def regular_strategy_frequency() -> int:
    return 100


@pytest.fixture
def random_strategy_trains_per_1000_seconds() -> float:
    return 10.0


@pytest.fixture
def random_strategy_seed() -> int:
    return 42


@pytest.fixture
def random_strategy_spawn_seconds() -> list[int]:
    # These are the seconds at which trains are spawned when using seed=42
    # and trains_per_1000_seconds=10.0
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
    ]


@pytest.fixture
def demand_strategy_spawn_seconds() -> list[int]:
    return [
        4600,
        7300,
        10900,
        13600,
        17200,
        20800,
        22600,
        25300,
        27100,
        32500,
        35200,
        37000,
        40600,
        42400,
        46000,
        50500,
        54100,
        57700,
        60400,
        63100,
        65800,
        68500,
        71200,
        73900,
        75700,
        80200,
        82900,
        86500,
        90100,
        92800,
        96400,
        98200,
        100900,
        104500,
        107200,
        109000,
        112600,
        118000,
        122500,
        127000,
        129700,
        132400,
        136900,
        140500,
        143200,
        145900,
        150400,
        155800,
        158500,
        162100,
        166600,
        170200,
        172000,
        177400,
        180100,
        182800,
        187300,
        190000,
        192700,
        195400,
        199000,
        201700,
        204400,
        208900,
        211600,
        214300,
        217900,
        221500,
        225100,
        229600,
        231400,
        234100,
        237700,
        241300,
        244900,
        247600,
        249400,
        253900,
        257500,
        261100,
        263800,
        267400,
        271000,
        274600,
        276400,
        280000,
        282700,
        287200,
        291700,
        296200,
        298000,
        300700,
        305200,
        307900,
        311500,
        315100,
        318700,
        322300,
        325900,
        328600,
        330400,
        334000,
        337600,
        341200,
        345700,
        348400,
        351100,
        353800,
        357400,
        360100,
        363700,
        366400,
        370000,
        374500,
        378100,
        380800,
        383500,
        387100,
        390700,
        392500,
        396100,
        398800,
        402400,
        406900,
        408700,
        412300,
        415900,
        420400,
        422200,
        426700,
        430300,
        433000,
        436600,
        442900,
        444700,
        448300,
        451000,
        453700,
        457300,
        460900,
        463600,
        467200,
        472600,
        475300,
        478900,
        482500,
        484300,
        487000,
        489700,
        494200,
        497800,
        502300,
        505000,
        506800,
        510400,
        513100,
        515800,
        519400,
        522100,
        526600,
        529300,
        532900,
        534700,
        537400,
        540100,
        543700,
        546400,
        550000,
        554500,
        557200,
        559900,
        562600,
        564400,
        567100,
        569800,
        572500,
        574300,
        577900,
        581500,
        584200,
        587800,
        590500,
        594100,
        597700,
        601300,
        604900,
        607600,
        609400,
        613000,
        615700,
        617500,
        620200,
        623800,
        627400,
        630100,
        632800,
        634600,
        638200,
        640900,
        644500,
        647200,
        650800,
        652600,
        656200,
        659800,
        662500,
        665200,
        670600,
        673300,
        676900,
        679600,
        683200,
        685000,
        688600,
        691300,
        694900,
        697600,
        701200,
        704800,
        709300,
        711100,
        714700,
        717400,
        719200,
        722800,
        725500,
        728200,
        731800,
        735400,
        738100,
        741700,
        745300,
        748000,
        751600,
        753400,
        756100,
        758800,
        760600,
        765100,
        768700,
        771400,
        775900,
        778600,
        781300,
        784000,
        786700,
        789400,
        795700,
        800200,
        803800,
        806500,
        810100,
        812800,
        815500,
        820000,
        824500,
        827200,
        830800,
        833500,
        837100,
        839800,
        843400,
        847900,
        850600,
        853300,
        857800,
        860500,
        862300,
        866800,
        870400,
        872200,
        875800,
        879400,
        882100,
        886600,
        890200,
        893800,
        896500,
        899200,
        902800,
        907300,
        910900,
        915400,
        919000,
        921700,
        925300,
        928000,
        930700,
        934300,
        937900,
        940600,
        943300,
        946900,
        949600,
        953200,
        956800,
        959500,
        962200,
        965800,
        968500,
        970300,
        974800,
        978400,
        982900,
        985600,
        988300,
        991900,
        995500,
        997300,
        1001800,
        1008100,
        1010800,
        1014400,
        1016200,
        1019800,
        1023400,
        1026100,
        1028800,
        1032400,
        1036000,
        1039600,
        1042300,
        1045000,
        1047700,
        1050400,
        1053100,
        1055800,
        1060300,
        1065700,
        1069300,
        1072900,
        1076500,
        1081000,
        1083700,
        1088200,
        1090900,
        1093600,
        1098100,
        1100800,
        1104400,
        1107100,
        1110700,
        1113400,
        1116100,
        1118800,
        1123300,
        1126900,
        1128700,
        1132300,
        1135000,
        1137700,
        1141300,
        1145800,
        1149400,
        1152100,
        1153900,
        1158400,
        1161100,
        1163800,
        1167400,
        1170100,
        1174600,
        1177300,
        1183600,
        1185400,
        1189000,
        1191700,
        1195300,
        1198900,
        1202500,
        1206100,
        1208800,
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
    strategy_start_time: int, strategy_end_time: int, regular_strategy_frequency: int
) -> dict[str, any]:
    return {
        "schedule_type": "TrainSchedule",
        "strategy_type": "RegularScheduleStrategy",
        "strategy_start_time": strategy_start_time,
        "strategy_end_time": strategy_end_time,
        "train_schedule_train_type": "passenger",
        "regular_strategy_frequency": regular_strategy_frequency,
    }


@pytest.fixture
def random_train_schedule_data(
    strategy_start_time: int,
    strategy_end_time: int,
    random_strategy_trains_per_1000_seconds: float,
    random_strategy_seed: int,
) -> dict[str, any]:
    return {
        "schedule_type": "TrainSchedule",
        "strategy_type": "RandomScheduleStrategy",
        "strategy_start_time": strategy_start_time,
        "strategy_end_time": strategy_end_time,
        "train_schedule_train_type": "cargo",
        "random_strategy_trains_per_1000_seconds": random_strategy_trains_per_1000_seconds,
        "random_strategy_seed": random_strategy_seed,
    }


@pytest.fixture
def demand_train_schedule_data(
    strategy_start_time: int,
    demand_strategy_power_station: str,
    demand_strategy_scaling_factor: float,
    demand_strategy_available_interval: tuple[datetime, datetime],
) -> dict[str, any]:
    seconds = (
        demand_strategy_available_interval[1] - demand_strategy_available_interval[0]
    ).total_seconds()
    return {
        "schedule_type": "TrainSchedule",
        "strategy_type": "DemandScheduleStrategy",
        "strategy_start_time": strategy_start_time,
        "strategy_end_time": strategy_start_time + int(seconds),
        "train_schedule_train_type": "cargo",
        "demand_strategy_power_station": demand_strategy_power_station,
        "demand_strategy_scaling_factor": demand_strategy_scaling_factor,
        "demand_strategy_start_datetime": demand_strategy_available_interval[0],
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
def random_train_schedule_configuration(
    random_train_schedule_data: dict[str, any], platform_ids: list[str]
) -> RandomScheduleStrategy:
    configuration = ScheduleConfiguration(**random_train_schedule_data)
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
    configuration = ScheduleConfiguration(**demand_train_schedule_data)
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
            self.spawn_history.append(int(identifier.split("_")[1]))
            self.identifier = identifier
            self.timetable = timetable
            self.train_type = train_type
            return True

        def let_next_spawn_fail(self):
            self._next_spawn_fails = True

    return MockTrainSpawner()


@pytest.fixture
def event_bus(run) -> EventBus:
    bus = EventBus(run_id=run.id)
    Logger(bus)
    return bus


@pytest.fixture
def spawner(
    spawner_configuration: SpawnerConfiguration,
    event_bus: EventBus,
    mock_train_spawner: object,
) -> Spawner:
    return Spawner(
        configuration=spawner_configuration,
        event_bus=event_bus,
        train_spawner=mock_train_spawner,
    )
