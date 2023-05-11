from typing import Callable

import pytest

from src.event_bus.event import Event, EventType
from src.event_bus.event_bus import EventBus


class TestEventBus:
    @pytest.fixture
    def event_bus(self) -> EventBus:
        return EventBus()

    @pytest.fixture
    def event_type(self) -> EventType:
        return EventType.TrainSpawn

    @pytest.fixture
    def callback(self) -> Callable[[Event], None]:
        def _callback(event: Event):
            pass

        return _callback

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

    def test_event(self, event_bus: EventBus, event_type: EventType):
        callback_called = False

        def callback(event: Event):
            callback_called = True
            assert event.event_type == event_type
            assert event.arguments["tick"] == 42
            assert event.arguments["train_id"] == "cool_train_id"

        event_bus.register_callback(callback, event_type)
        event_bus.spawn_train(42, train_id="cool_train_id")
        assert callback_called

    def test_wrong_arguments(
        self,
        event_bus: EventBus,
        event_type: EventType,
        callback: Callable[[Event], None],
    ):
        event_bus.register_callback(callback, event_type)
        with pytest.raises(AttributeError):
            event_bus.spawn_train(42, train_id="cool_train_id", wrong_argument="foo")
