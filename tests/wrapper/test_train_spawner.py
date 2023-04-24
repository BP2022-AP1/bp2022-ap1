import pytest

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.train_spawner import TrainSpawner


def test_spawn_train(souc: SimulationObjectUpdatingComponent, spawner: TrainSpawner):
    assert spawner.spawn_train("test-train-1", ["station-1", "station-2"], "test-cargo")

    assert len(souc.trains) == 1


def test_spawn_train_no_route(
    souc: SimulationObjectUpdatingComponent, spawner2: TrainSpawner
):
    assert not spawner2.spawn_train(
        "test-train-2", ["station-2", "station-0"], "test-cargo"
    )

    assert len(souc.trains) == 0
