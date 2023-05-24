from typing import Tuple

import pytest

from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.fault_injector.fault_strategies import (
    RandomFaultStrategy,
    RegularFaultStrategy,
)


class TestFaultStrategies:
    """ Test fault strategies
    """
    @pytest.fixture
    def regular_ticks(self):
        return (4, 109)

    @pytest.fixture
    def seed(self):
        return 42

    @pytest.fixture
    def random_inject_ticks(self):
        return [
            1,
            2,
            3,
            7,
            9,
            10,
            12,
            13,
            16,
            19,
            22,
            23,
            25,
            26,
            27,
            34,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            49,
            50,
            51,
            52,
            56,
            58,
            59,
            66,
            67,
            68,
            69,
            70,
            73,
            75,
            78,
            79,
            81,
            84,
            85,
            88,
            89,
            90,
            94,
            95,
            100,
            104,
            106,
            111,
            113,
            116,
            119,
            124,
            125,
            126,
            130,
            131,
            134,
            136,
            139,
            142,
            145,
            148,
            149,
            154,
            155,
            156,
            158,
            159,
            160,
            162,
            165,
            166,
            168,
            169,
            175,
            176,
            183,
            184,
            185,
            187,
            188,
            191,
            192,
            197,
        ]

    @pytest.fixture
    def random_resolve_ticks(self):
        return [
            0,
            1,
            2,
            3,
            4,
            5,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            19,
            21,
            22,
            23,
            25,
            26,
            27,
            29,
            31,
            32,
            34,
            35,
            37,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            54,
            55,
            56,
            57,
            58,
            59,
            61,
            62,
            63,
            66,
            67,
            68,
            69,
            70,
            73,
            74,
            75,
            77,
            78,
            79,
            80,
            81,
            82,
            84,
            85,
            87,
            88,
            89,
            90,
            91,
            93,
            94,
            95,
            97,
            100,
            101,
            102,
            103,
            104,
            105,
            106,
            107,
            108,
            111,
            112,
            113,
            116,
            117,
            118,
            119,
            120,
            121,
            123,
            124,
            125,
            126,
            130,
            131,
            134,
            135,
            136,
            137,
            138,
            139,
            140,
            141,
            142,
            144,
            145,
            146,
            147,
            148,
            149,
            151,
            152,
            153,
            154,
            155,
            156,
            157,
            158,
            159,
            160,
            161,
            162,
            165,
            166,
            167,
            168,
            169,
            171,
            172,
            175,
            176,
            177,
            178,
            179,
            180,
            181,
            183,
            184,
            185,
            187,
            188,
            189,
            190,
            191,
            192,
            194,
            196,
            197,
        ]

    @pytest.fixture
    def regular_fault_strategy(self):
        return RegularFaultStrategy()

    @pytest.fixture
    def random_fault_strategy(self, seed):
        return RandomFaultStrategy(seed=seed)

    @pytest.fixture
    def regular_configuration(self, regular_ticks):
        return FaultConfiguration(
            **{
                "start_tick": regular_ticks[0],
                "end_tick": regular_ticks[1],
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def random_configuration(self):
        return FaultConfiguration(
            **{
                "inject_probability": 0.42,
                "resolve_probability": 0.77,
                "strategy": "random",
            }
        )

    def test_regular_strategy(
        self,
        regular_fault_strategy: RegularFaultStrategy,
        regular_configuration: FaultConfiguration,
        regular_ticks: Tuple[int, int],
    ):
        for tick in range(200):
            assert regular_fault_strategy.should_inject(
                tick, regular_configuration, False
            ) == (tick == regular_ticks[0])
            assert not regular_fault_strategy.should_resolve(
                tick, regular_configuration, False
            )
        for tick in range(200):
            assert not regular_fault_strategy.should_inject(
                tick, regular_configuration, True
            )
            assert regular_fault_strategy.should_resolve(
                tick, regular_configuration, True
            ) == (tick == regular_ticks[1])

    def test_inject_random_strategy(
        self,
        random_fault_strategy: RandomFaultStrategy,
        random_configuration: FaultConfiguration,
        random_inject_ticks: list[float],
    ):
        injected = False
        for tick in range(200):
            if tick > 99:
                injected = True
            if random_fault_strategy.should_inject(
                tick, random_configuration, injected
            ):
                assert tick in random_inject_ticks and not injected

    def test_resolve_random_strategy(
        self,
        random_fault_strategy: RandomFaultStrategy,
        random_configuration: FaultConfiguration,
        random_resolve_ticks: list[float],
    ):
        injected = False
        for tick in range(200):
            if tick > 99:
                injected = True
            if random_fault_strategy.should_resolve(
                tick, random_configuration, injected
            ):
                assert tick in random_resolve_ticks and injected
