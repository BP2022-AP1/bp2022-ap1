from typing import Tuple

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.train_builder import TrainBuilder


def test_spawn_train(spawner: Tuple[SimulationObjectUpdatingComponent, TrainBuilder]):
    (souc, spawner) = spawner
    assert spawner.spawn_train("test-train-1", ["station-1", "station-2"], "test-cargo")

    assert len(souc.trains) == 1

    assert spawner[1].route_controller.reserve_for_initialized_train_count == 1
    assert spawner[1].route_controller.set_spawn_fahrstrasse_count == 1


def test_spawn_train_no_route(
    spawner: Tuple[SimulationObjectUpdatingComponent, TrainBuilder]
):
    (souc, spawner) = spawner
    assert not spawner.spawn_train(
        "test-train-2", ["station-2", "station-0"], "test-cargo"
    )

    assert len(souc.trains) == 0
