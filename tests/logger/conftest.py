import pytest

from src.event_bus.event_bus import EventBus


@pytest.fixture
def event_bus() -> EventBus:
    return EventBus(run_id=42)
