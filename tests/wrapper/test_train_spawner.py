import pytest

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.train_spawner import TrainSpawner


def test_spawn_train(souc: SimulationObjectUpdatingComponent, spawner: TrainSpawner):
    assert spawner.spawn_train("test-train-1", ["1", "2"], "test-cargo")


def test_spawn_train_no_route(
    souc: SimulationObjectUpdatingComponent, spawner2: TrainSpawner
):
    assert not spawner2.spawn_train("test-train-1", ["1", "2"], "test-cargo")
