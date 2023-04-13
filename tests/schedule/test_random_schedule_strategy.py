import pytest

from src.schedule.random_schedule_strategy import RandomScheduleStrategy


class TestRandomScheduleStrategy:
    """Test the random schedule strategy"""

    @pytest.fixture
    def start_tick(self) -> int:
        return 100

    @pytest.fixture
    def end_tick(self) -> int:
        return 2000

    @pytest.fixture
    def probability(self) -> float:
        return 10.0

    @pytest.fixture
    def seed(self) -> int:
        return 42

    @pytest.fixture
    def spawn_ticks(self) -> list[int]:
        # These are the ticks at which trains are spawned when using seed=42
        # and trains_per_1000_ticks=10.0
        return [
            119,
            224,
            369,
            390,
            397,
            468,
            494,
            527,
            581,
            784,
            982,
            1126,
            1233,
            1268,
            1274,
            1491,
            1907,
            1936,
        ]

    @pytest.fixture
    def random_strategy(
        self, start_tick: int, end_tick: int, probability: float, seed: int
    ) -> RandomScheduleStrategy:
        return RandomScheduleStrategy(
            start_tick=start_tick,
            end_tick=end_tick,
            trains_per_1000_ticks=probability,
            seed=seed,
        )

    def test_spawn_at_right_ticks(
        self,
        random_strategy: RandomScheduleStrategy,
        spawn_ticks: list[int],
        end_tick: int,
    ):
        for tick in range(0, end_tick * 2):
            if random_strategy.should_spawn(tick):
                assert tick in spawn_ticks
