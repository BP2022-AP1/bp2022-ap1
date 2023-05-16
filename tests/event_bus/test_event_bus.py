from typing import Callable

import pytest

from src.event_bus.event import Event, EventType
from src.event_bus.event_bus import EventBus


class TestEventBus:
    """Tests for the EventBus"""

    @pytest.fixture
    def event_bus(self, run) -> EventBus:
        return EventBus(run_id=run.id)

    @pytest.fixture
    def event_type(self) -> EventType:
        return EventType.TRAIN_SPAWN

    @pytest.fixture
    def callback(self) -> Callable[[Event], None]:
        def _callback(event: Event):
            pass

        return _callback

    @pytest.fixture
    def tick(self) -> int:
        return 42

    @pytest.fixture
    def train_id(self) -> str:
        return "cool_train_id"

    def test_register_callback(
        self,
        event_bus: EventBus,
        event_type: EventType,
        callback: Callable[[Event], None],
    ):
        handle = event_bus.register_callback(callback, event_type)
        assert handle in event_bus.callbacks
        assert event_bus.callbacks[handle][0] == callback
        assert event_bus.callbacks[handle][1] == event_type

    def test_unregister_callback(
        self,
        event_bus: EventBus,
        event_type: EventType,
        callback: Callable[[Event], None],
    ):
        handle = event_bus.register_callback(callback, event_type)
        event_bus.unregister_callback(handle)
        assert len(event_bus.callbacks.keys()) == 0

    def test_event(
        self, event_bus: EventBus, event_type: EventType, tick: int, train_id: str
    ):
        self.callback_called = False

        def callback(event: Event):
            self.callback_called = True
            assert event.event_type == event_type
            assert event.arguments["tick"] == tick
            assert event.arguments["train_id"] == train_id

        event_bus.register_callback(callback, event_type)
        event_bus.spawn_train(tick, train_id=train_id)
        assert self.callback_called

    def test_wrong_method(
        self,
        event_bus: EventBus,
        event_type: EventType,
        callback: Callable[[Event], None],
        tick: int,
        train_id: str,
    ):
        event_bus.register_callback(callback, event_type)
        with pytest.raises(AttributeError):
            event_bus.wrong_method(tick, train_id=train_id)

    def test_wrong_number_of_arguments(
        self,
        event_bus: EventBus,
        event_type: EventType,
        callback: Callable[[Event], None],
        tick: int,
    ):
        event_bus.register_callback(callback, event_type)
        with pytest.raises(TypeError):
            event_bus.spawn_train(tick)

    def test_wrong_keyword_argument(
        self,
        event_bus: EventBus,
        event_type: EventType,
        callback: Callable[[Event], None],
        tick: int,
    ):
        event_bus.register_callback(callback, event_type)
        with pytest.raises(TypeError):
            event_bus.spawn_train(tick, wrong_keyword="wrong_keyword")
