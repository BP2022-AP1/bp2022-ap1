from typing import Tuple

from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.train_builder import TrainBuilder


def test_spawn_train(spawner: Tuple[SimulationObjectUpdatingComponent, TrainBuilder]):
    (souc, train_spawner) = spawner
    assert train_spawner.spawn_train(
        "test-train-1", ["bs_3", "bs_2"], "test-cargo"
    )

    assert len(souc.trains) == 1

    assert train_spawner.route_controller.set_spawn_fahrstrasse_count == 1
    assert train_spawner.route_controller.reserve_for_initialized_train_count == 1


def test_spawn_train_no_route(
    spawner: Tuple[SimulationObjectUpdatingComponent, TrainBuilder]
):
    (souc, train_spawner) = spawner
    assert not train_spawner.spawn_train(
        "test-train-2", ["bs_0", "bs_1"], "test-cargo"
    )

    assert len(souc.trains) == 0

    assert train_spawner.route_controller.set_spawn_fahrstrasse_count == 1
    assert train_spawner.route_controller.reserve_for_initialized_train_count == 0
