from typing import Tuple

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.train_builder import TrainBuilder


def test_spawn_train(spawner: Tuple[SimulationObjectUpdatingComponent, TrainBuilder]):
    (souc, unboxed_spawner) = spawner
    assert unboxed_spawner.spawn_train(
        "test-train-1", ["station-1", "station-2"], "test-cargo"
    )

    assert len(souc.trains) == 1


def test_spawn_train_no_route(
    spawner: Tuple[SimulationObjectUpdatingComponent, TrainBuilder]
):
    (souc, unboxed_spawner) = spawner
    assert not unboxed_spawner.spawn_train(
        "test-train-2", ["station-2", "station-0"], "test-cargo"
    )

    assert len(souc.trains) == 0
