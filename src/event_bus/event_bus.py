from typing import Callable, Iterator
from uuid import UUID, uuid4

from src.event_bus.event import Event, EventType


class EventBus:
    """A class that creates events and distributes them among
    its subscribers.
    """

    # This dict contains the names of all event producing methods
    # (aka methods the Logger implements) as keys. The values are tuples
    # containing the argument names and the associated EventType
    EVENT_METHODS: dict[str, tuple[list[str], EventType]] = {
        "spawn_train": (["tick", "train_id"], EventType.TrainSpawn),
        "remove_train": (["tick", "train_id"], EventType.TrainRemove),
        "arrival_train": (["tick", "train_id", "station_id"], EventType.TrainArrival),
        "departure_train": (
            ["tick", "train_id", "station_id"],
            EventType.TrainDeparture,
        ),
        "create_fahrstrasse": (["tick", "fahrstrasse"], EventType.CreateFahrstrasse),
        "remove_fahrstrasse": (["tick", "farhstrasse"], EventType.RemoveFahrstrasse),
        "set_signal": (
            ["tick", "signal_id", "state_before", "state_after"],
            EventType.SetSignal,
        ),
        "train_enter_block_section": (
            ["tick", "train_id", "block_section_id", "block_section_length"],
            EventType.TrainEnterBlockSection,
        ),
        "train_leave_block_section": (
            ["tick", "train_id", "block_section_id", "block_section_length"],
            EventType.TrainLeaveBlockSection,
        ),
        "inject_platform_blocked_fault": (
            ["tick", "platform_blocked_fault_configuration", "affected_element"],
            EventType.InjectFault,
        ),
        "inject_track_blocked_fault": (
            ["tick", "track_blocked_fault_configuration", "affected_element"],
            EventType.InjectFault,
        ),
        "inject_track_speed_limit_fault": (
            [
                "tick",
                "track_speed_limit_fault_configuration",
                "affected_element",
                "value_before",
                "value_after",
            ],
            EventType.InjectFault,
        ),
        "inject_schedule_blocked_fault": (
            ["tick", "schedule_blocked_fault_configuration", "affected_element"],
            EventType.InjectFault,
        ),
        "inject_train_prio_fault": (
            [
                "tick",
                "train_prio_fault_configuration",
                "affected_element",
                "value_before",
                "value_after",
            ],
            EventType.InjectFault,
        ),
        "inject_train_speed_fault": (
            [
                "tick",
                "train_speed_fault_configuration",
                "affected_element",
                "value_before",
                "value_after",
            ],
            EventType.InjectFault,
        ),
        "resolve_platform_blocked_fault": (
            ["tick", "platform_blocked_fault_configuration"],
            EventType.ResolveFault,
        ),
        "resolve_track_blocked_fault": (
            ["tick", "track_blocked_fault_configuration"],
            EventType.ResolveFault,
        ),
        "resolve_track_speed_limit_fault": (
            ["tick", "track_speed_limit_fault_configuration"],
            EventType.ResolveFault,
        ),
        "resolve_schedule_blocked_fault": (
            ["tick", "schedule_blocked_fault_configuration"],
            EventType.ResolveFault,
        ),
        "resolve_train_prio_fault": (
            ["tick", "train_prio_fault_configuration"],
            EventType.ResolveFault,
        ),
        "resolve_train_speed_fault": (
            ["tick", "train_speed_fault_configuration"],
            EventType.ResolveFault,
        ),
    }

    callbacks: dict[UUID, tuple[Callable[[Event], None], EventType]]

    def __init__(self):
        self.callbacks = {}

    def register_callback(
        self, callback: Callable[[Event], None], event_type: EventType
    ) -> UUID:
        """Subscribe to an event type

        :param callback: A callable that gets called when the event is triggered
        :param event_type: The type of the event
        :return: A handle to this subscription
        """
        handle = uuid4()
        self.callbacks[handle] = (callback, event_type)
        return handle

    def unregister_callback(self, handle: UUID):
        """Cancels the subscription associated to a handle

        :param handle: the handle
        """
        self.callbacks.pop(handle)

    def _get_callbacks_for_event_type(
        self, event_type: EventType
    ) -> Iterator[Callable[[Event], None]]:
        """Returns an iterator to all callbacks associated with th eenevent type

        :param event_type: The event type
        :return: The iterator to all the callbacks
        :yield: a callback
        """
        return (callback for callback, e_type in self.callbacks if e_type == event_type)

    def _build_arguments(self, arg_keys: list[str], args: list, kwargs: dict) -> dict:
        """Constructs an argument dict from a list of keys that have to be included
        a list of argument values and an kwargs-dict

        :param arg_keys: the list of keys
        :param args: the list of values
        :param kwargs: the kwargs dict
        :return: the argument dict
        """
        assert len(args) + len(kwargs.keys()) == len(arg_keys)
        arguments = {key: value for key, value in zip(arg_keys, args)}
        arg_keys = [key for key in arg_keys if key not in arguments]
        assert set(arg_keys) == set(kwargs.keys())
        return arguments | kwargs

    def __getattr__(self, name: str) -> object:
        """This pretends to a caller that the class has the methods
        defined in EVENT_METHODS. It returns a callable that creates
        an event and calls all callbacks.

        :param name: the method name
        :raises AttributeError: when unknown method name is passed
        :return: a callable
        """
        if name not in self.EVENT_METHODS:
            raise AttributeError(f"EventBus has no attribute {name}")
        arg_keys, event_type = self.EVENT_METHODS[name]

        def emit_event(*args: list, **kwargs: dict):
            arguments = self._build_arguments(arg_keys, args, kwargs)
            event = Event(event_type, arguments)
            for callback in self._get_callbacks_for_event_type(event_type):
                callback(event)

        return emit_event
