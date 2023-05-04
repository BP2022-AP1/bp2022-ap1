import uuid

import pytest

from src import implementor as impl
from src.implementor.models import Run


class TestRunImplementor:
    def test_get_all_simulation_ids(self, token, empty_simulation_configuration):
        run = Run.create(simulation_configuration=empty_simulation_configuration)
        result, status = impl.run.get_all_run_ids({}, token)
        assert status == 200
        assert str(run.id) in result

    def test_get_all_simulation_ids_option(
        self,
        token,
        empty_simulation_configuration,
        another_empty_simulation_configuration,
    ):
        run = Run.create(simulation_configuration=empty_simulation_configuration)
        another_run = Run.create(
            simulation_configuration=another_empty_simulation_configuration
        )
        result, status = impl.run.get_all_run_ids(
            {"simulationId": empty_simulation_configuration.id}, token
        )
        assert status == 200
        assert str(run.id) in result
        assert str(another_run.id) not in result

    def test_get_all_simulation_ids_not_found(self, token):
        result, status = impl.run.get_all_run_ids(
            {"simulationId": str(uuid.uuid4())}, token
        )
        assert status == 404
        assert result == "Simulation not found"
