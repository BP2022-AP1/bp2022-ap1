import pytest

from src.implementor.models import SimulationConfiguration, Token
from src.interlocking_component.interlocking_configuration import (
    InterlockingConfiguration,
)


@pytest.fixture
def token() -> Token:
    token = Token(name="owner", permission="admin", hashedToken="hash")
    token.save()
    return token


@pytest.fixture
def simulation_configuration() -> SimulationConfiguration:
    config = SimulationConfiguration()
    config.save()
    return config


def interlocking_configuration() -> InterlockingConfiguration:
    config = InterlockingConfiguration(
        dynamicRouting=True,
    )
    config.save()
    return config
