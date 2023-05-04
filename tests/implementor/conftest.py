import hashlib

import pytest

from src.implementor.models import Run, SimulationConfiguration, Token


@pytest.fixture
def token():
    clear_token = "token"
    hashed_token = hashlib.sha256(clear_token.encode()).hexdigest()
    name = "user"
    permission = "user"
    return Token.create(name=name, permission=permission, hashedToken=hashed_token)


@pytest.fixture
def empty_simulation_configuration():
    simulation = SimulationConfiguration()
    simulation.save()
    return simulation


@pytest.fixture
def another_empty_simulation_configuration():
    simulation = SimulationConfiguration()
    simulation.save()
    return simulation
