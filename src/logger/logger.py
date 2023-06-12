"""
This module contains the logger class
"""
from datetime import datetime
from typing import Type
from uuid import UUID

from src.component import Component
from src.event_bus.event import Event, EventType
from src.event_bus.event_bus import EventBus
from src.logger.log_entry import (
    CreateFahrstrasseLogEntry,
    InjectFaultLogEntry,
    RemoveFahrstrasseLogEntry,
    ResolveFaultLogEntry,
    SetSignalLogEntry,
    TrainArrivalLogEntry,
    TrainDepartureLogEntry,
    TrainEnterBlockSectionLogEntry,
    TrainLeaveBlockSectionLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)


# pylint: disable=too-many-public-methods
class Logger(Component):
    """
    The logger class is used to log the events of the simulation
    """

    callback_handles: list[UUID]

    def __init__(self, event_bus: EventBus):
        """
        The constructor of the logger class
        """
        super().__init__(event_bus, "LOW")

        self.callback_handles = []
        self.callback_handles.append(
            self.event_bus.register_callback(self.spawn_train, EventType.TRAIN_SPAWN)
        )
        self.callback_handles.append(
            self.event_bus.register_callback(self.remove_train, EventType.TRAIN_REMOVE)
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.arrival_train, EventType.TRAIN_ARRIVAL
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.departure_train, EventType.TRAIN_DEPARTURE
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.create_fahrstrasse, EventType.CREATE_FAHRSTRASSE
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.remove_fahrstrasse, EventType.REMOVE_FAHRSTRASSE
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(self.set_signal, EventType.SET_SIGNAL)
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.train_enter_block_section, EventType.TRAIN_ENTER_BLOCK_SECTION
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.train_leave_block_section, EventType.TRAIN_LEAVE_BLOCK_SECTION
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.inject_platform_blocked_fault, EventType.INJECT_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.inject_track_blocked_fault, EventType.INJECT_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.inject_track_speed_limit_fault, EventType.INJECT_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.inject_schedule_blocked_fault, EventType.INJECT_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.inject_train_prio_fault, EventType.INJECT_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.inject_train_speed_fault, EventType.INJECT_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.resolve_platform_blocked_fault, EventType.RESOLVE_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.resolve_track_blocked_fault, EventType.RESOLVE_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.resolve_track_speed_limit_fault, EventType.RESOLVE_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.resolve_schedule_blocked_fault, EventType.RESOLVE_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.resolve_train_prio_fault, EventType.RESOLVE_FAULT
            )
        )
        self.callback_handles.append(
            self.event_bus.register_callback(
                self.resolve_train_speed_fault, EventType.RESOLVE_FAULT
            )
        )

    def __del__(self):
        for handle in self.callback_handles:
            self.event_bus.unregister_callback(handle)

    def next_tick(self, tick: int):
        pass

    def spawn_train(self, event: Event) -> Type[None]:
        """
        This function should be called when a train is being spawned. This should include a train
        identifier.
        :param event: the event containing all relevant info
        """
        TrainSpawnLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train with ID {event.arguments['train_id']} spawned",
            run_id=self.event_bus.run_id,
            train_id=event.arguments["train_id"],
        )

    def remove_train(self, event: Event) -> Type[None]:
        """
        This function should be called when a train is being removed. This should include a train
        identifier.
        :param event: the event containing all relevant info
        """
        TrainRemoveLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train with ID {event.arguments['train_id']} removed",
            run_id=self.event_bus.run_id,
            train_id=event.arguments["train_id"],
        )

    def arrival_train(self, event: Event) -> Type[None]:
        """
        This function should be called when a train arrives at a station. This should include a
        train identifier and the station identifier.
        :param event: the event containing all relevant info
        """
        TrainArrivalLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train with ID {event.arguments['train_id']} "
            f"arrived at station with ID {event.arguments['station_id']}",
            run_id=self.event_bus.run_id,
            train_id=event.arguments["train_id"],
            station_id=event.arguments["station_id"],
        )

    def departure_train(self, event: Event) -> Type[None]:
        """
        This function should be called when a train departs from a station. This should include a
        train identifier and the station identifier.
        :param event: the event containing all relevant info
        """
        TrainDepartureLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train with ID {event.arguments['train_id']} departed from "
            f"station with ID {event.arguments['station_id']}",
            run_id=self.event_bus.run_id,
            train_id=event.arguments["train_id"],
            station_id=event.arguments["station_id"],
        )

    def create_fahrstrasse(self, event: Event) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is being formed. This should include the
        definition of the Fahrstrasse.
        :param event: the event containing all relevant info
        """
        CreateFahrstrasseLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Fahrstrasse {event.arguments['fahrstrasse']} created",
            run_id=self.event_bus.run_id,
            fahrstrasse=event.arguments["fahrstrasse"],
        )

    def remove_fahrstrasse(self, event: Event) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is being dissolved. This should include
        the definition of the Fahrstrasse.
        :param event: the event containing all relevant info
        """
        RemoveFahrstrasseLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Fahrstrasse {event.arguments['fahrstrasse']} removed",
            run_id=self.event_bus.run_id,
            fahrstrasse=event.arguments["fahrstrasse"],
        )

    def set_signal(self, event: Event) -> Type[None]:
        """
        This function is being called when setting a signal or changing its state. This should
        include the signal identifier, the state before and the state after the change.
        :param event: the event containing all relevant info
        """
        SetSignalLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Signal with ID {event.arguments['signal_id']} changed "
            f"from {event.arguments['state_before']} to {event.arguments['state_after']}",
            run_id=self.event_bus.run_id,
            signal_id=event.arguments["signal_id"],
            state_before=event.arguments["state_before"],
            state_after=event.arguments["state_after"],
        )

    def train_enter_block_section(self, event: Event) -> Type[None]:
        """
        This function should be called when a train enters a block section. This should include a
        train identifier, the block section identifier and the length of the block section.
        :param event: the event containing all relevant info
        """
        TrainEnterBlockSectionLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train with ID {event.arguments['train_id']} entered block "
            f"section with ID {event.arguments['block_section_id']} "
            f"with length {event.arguments['block_section_length']}",
            run_id=self.event_bus.run_id,
            train_id=event.arguments["train_id"],
            block_section_id=event.arguments["block_section_id"],
            block_section_length=event.arguments["block_section_length"],
        )

    def train_leave_block_section(self, event: Event) -> Type[None]:
        """
        This function should be called when a train leaves a block section. This should include a
        train identifier, the block section identifier and the length of the block section.
        :param event: the event containing all relevant info
        """
        TrainLeaveBlockSectionLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train with ID {event.arguments['train_id']} left block "
            f"section with ID {event.arguments['block_section_id']}",
            run_id=self.event_bus.run_id,
            train_id=event.arguments["train_id"],
            block_section_id=event.arguments["block_section_id"],
            block_section_length=event.arguments["block_section_length"],
        )

    def inject_platform_blocked_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when injecting a platform blocked fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param event: the event containing all relevant info
        """
        if "platform_blocked_fault_configuration" not in event.arguments:
            return
        InjectFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Platform blocked fault with configuration "
            f"{event.arguments['platform_blocked_fault_configuration']} on "
            f"element {event.arguments['affected_element']}",
            run_id=self.event_bus.run_id,
            platform_blocked_fault_configuration=event.arguments[
                "platform_blocked_fault_configuration"
            ],
            affected_element=event.arguments["affected_element"],
        )

    def inject_track_blocked_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when injecting a track blocked fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param event: the event containing all relevant info
        """
        if "track_blocked_fault_configuration" not in event.arguments:
            return
        InjectFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Track blocked fault with configuration "
            f"{event.arguments['track_blocked_fault_configuration']} "
            f"on element {event.arguments['affected_element']}",
            run_id=self.event_bus.run_id,
            track_blocked_fault_configuration=event.arguments[
                "track_blocked_fault_configuration"
            ],
            affected_element=event.arguments["affected_element"],
        )

    def inject_track_speed_limit_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when injecting a track speed limit fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param event: the event containing all relevant info
        """
        if "track_speed_limit_fault_configuration" not in event.arguments:
            return
        InjectFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Track speed limit fault with configuration "
            f"{event.arguments['track_speed_limit_fault_configuration']} "
            f"on element {event.arguments['affected_element']} "
            f"changed from {event.arguments['value_before']} to {event.arguments['value_after']}",
            run_id=self.event_bus.run_id,
            track_speed_limit_fault_configuration=event.arguments[
                "track_speed_limit_fault_configuration"
            ],
            affected_element=event.arguments["affected_element"],
            value_before=event.arguments["value_before"],
            value_after=event.arguments["value_after"],
        )

    def inject_schedule_blocked_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when injecting a train speed fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param event: the event containing all relevant info
        """
        if "schedule_blocked_fault_configuration" not in event.arguments:
            return
        InjectFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Schedule blocked fault with configuration "
            f"{event.arguments['schedule_blocked_fault_configuration']} on "
            f"element {event.arguments['affected_element']}",
            run_id=self.event_bus.run_id,
            schedule_blocked_fault_configuration=event.arguments[
                "schedule_blocked_fault_configuration"
            ],
            affected_element=event.arguments["affected_element"],
        )

    def inject_train_prio_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when injecting a train prio fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param event: the event containing all relevant info
        """
        if "train_prio_fault_configuration" not in event.arguments:
            return
        InjectFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train prio fault with configuration "
            f"{event.arguments['train_prio_fault_configuration']} "
            f"on element {event.arguments['affected_element']} changed from "
            f"{event.arguments['value_before']} to {event.arguments['value_after']}",
            run_id=self.event_bus.run_id,
            train_prio_fault_configuration=event.arguments[
                "train_prio_fault_configuration"
            ],
            affected_element=event.arguments["affected_element"],
            value_before=event.arguments["value_before"],
            value_after=event.arguments["value_after"],
        )

    def inject_train_speed_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when injecting a train speed fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param event: the event containing all relevant info
        """
        if "train_speed_fault_configuration" not in event.arguments:
            return
        InjectFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train speed fault with configuration "
            f"{event.arguments['train_speed_fault_configuration']} "
            f"on element {event.arguments['affected_element']} changed from "
            f"{event.arguments['value_before']} to {event.arguments['value_after']}",
            run_id=self.event_bus.run_id,
            train_speed_fault_configuration=event.arguments[
                "train_speed_fault_configuration"
            ],
            affected_element=event.arguments["affected_element"],
            value_before=event.arguments["value_before"],
            value_after=event.arguments["value_after"],
        )

    def resolve_platform_blocked_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when removing a platform blocked fault from the simulation.
        This should reference the fault configuration of the fault.
        :param event: the event containing all relevant info
        """
        if "platform_blocked_fault_configuration" not in event.arguments:
            return
        ResolveFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Platform blocked fault with configuration "
            f"{event.arguments['platform_blocked_fault_configuration']} resolved",
            run_id=self.event_bus.run_id,
            platform_blocked_fault_configuration=event.arguments[
                "platform_blocked_fault_configuration"
            ],
        )

    def resolve_track_blocked_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when removing a track blocked fault from the simulation.
        This should reference the fault configuration of the fault.
        :param event: the event containing all relevant info
        """
        if "track_blocked_fault_configuration" not in event.arguments:
            return
        ResolveFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Track blocked fault with configuration "
            f"{event.arguments['track_blocked_fault_configuration']} resolved",
            run_id=self.event_bus.run_id,
            track_blocked_fault_configuration=event.arguments[
                "track_blocked_fault_configuration"
            ],
        )

    def resolve_track_speed_limit_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when removing a track speed limit fault from the simulation.
        This should reference the fault configuration of the fault.
        :param event: the event containing all relevant info
        """
        if "track_speed_limit_fault_configuration" not in event.arguments:
            return
        ResolveFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Track speed limit fault with configuration "
            f"{event.arguments['track_speed_limit_fault_configuration']} resolved",
            run_id=self.event_bus.run_id,
            track_speed_limit_fault_configuration=event.arguments[
                "track_speed_limit_fault_configuration"
            ],
        )

    def resolve_schedule_blocked_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when removing a schedule blocked fault from the simulation.
        This should reference the fault configuration of the fault.
        :param event: the event containing all relevant info
        """
        if "schedule_blocked_fault_configuration" not in event.arguments:
            return
        ResolveFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Schedule blocked fault with configuration "
            f"{event.arguments['schedule_blocked_fault_configuration']} resolved",
            run_id=self.event_bus.run_id,
            schedule_blocked_fault_configuration=event.arguments[
                "schedule_blocked_fault_configuration"
            ],
        )

    def resolve_train_prio_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when removing a train prio fault from the simulation.
        This should reference the fault configuration of the fault.
        :param event: the event containing all relevant info
        """
        if "train_prio_fault_configuration" not in event.arguments:
            return
        ResolveFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train prio fault with configuration "
            f"{event.arguments['train_prio_fault_configuration']} resolved",
            run_id=self.event_bus.run_id,
            train_prio_fault_configuration=event.arguments[
                "train_prio_fault_configuration"
            ],
        )

    def resolve_train_speed_fault(self, event: Event) -> Type[None]:
        """
        This function should be called when removing a train speed fault from the simulation. This
        should reference the fault configuration of the fault.
        :param event: the event containing all relevant info
        """
        if "train_speed_fault_configuration" not in event.arguments:
            return
        ResolveFaultLogEntry.create(
            timestamp=datetime.now(),
            tick=event.arguments["tick"],
            message=f"Train speed fault with configuration "
            f"{event.arguments['train_speed_fault_configuration']} resolved",
            run_id=self.event_bus.run_id,
            train_speed_fault_configuration=event.arguments[
                "train_speed_fault_configuration"
            ],
        )
