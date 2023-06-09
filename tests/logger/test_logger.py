from datetime import datetime

from freezegun import freeze_time

from src.event_bus.event import Event, EventType
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
from src.logger.logger import Logger
from tests.decorators import recreate_db_setup


# pylint: disable=too-many-public-methods
class TestLogger:
    """Class for testing logger functions."""

    @recreate_db_setup
    def setup_method(self):
        pass

    @freeze_time()
    def test_spawn_train(self, run, tick, train_id, event_bus):
        event = Event(EventType.TRAIN_SPAWN, {"tick": tick, "train_id": train_id})
        logger = Logger(event_bus=event_bus)
        logger.spawn_train(event)
        log_entry = (
            TrainSpawnLogEntry.select()
            .where(TrainSpawnLogEntry.train_id == train_id)
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Train with ID {train_id} spawned"
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id

    @freeze_time()
    def test_remove_train(self, run, tick, train_id, event_bus):
        event = Event(EventType.TRAIN_REMOVE, {"tick": tick, "train_id": train_id})
        logger = Logger(event_bus=event_bus)
        logger.remove_train(event)
        log_entry = (
            TrainRemoveLogEntry.select()
            .where(TrainRemoveLogEntry.train_id == train_id)
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Train with ID {train_id} removed"
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id

    @freeze_time()
    def test_arrival_train(self, run, tick, train_id, station_id, event_bus):
        event = Event(
            EventType.TRAIN_ARRIVAL,
            {"tick": tick, "train_id": train_id, "station_id": station_id},
        )
        logger = Logger(event_bus=event_bus)
        logger.arrival_train(event)
        log_entry = (
            TrainArrivalLogEntry.select()
            .where(
                (TrainArrivalLogEntry.tick == tick)
                & (TrainArrivalLogEntry.train_id == train_id)
                & (TrainArrivalLogEntry.station_id == station_id)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train with ID {train_id} arrived at station with ID {station_id}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
        assert log_entry.station_id == station_id

    @freeze_time()
    def test_departure_train(self, run, tick, train_id, station_id, event_bus):
        event = Event(
            EventType.TRAIN_DEPARTURE,
            {"tick": tick, "train_id": train_id, "station_id": station_id},
        )
        logger = Logger(event_bus=event_bus)
        logger.departure_train(event)
        log_entry = (
            TrainDepartureLogEntry.select()
            .where(
                (TrainDepartureLogEntry.tick == tick)
                & (TrainDepartureLogEntry.train_id == train_id)
                & (TrainDepartureLogEntry.station_id == station_id)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train with ID {train_id} departed from station with ID {station_id}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
        assert log_entry.station_id == station_id

    @freeze_time()
    def test_create_fahrstrasse(self, run, tick, fahrstrasse, event_bus):
        event = Event(
            EventType.CREATE_FAHRSTRASSE, {"tick": tick, "fahrstrasse": fahrstrasse}
        )
        logger = Logger(event_bus=event_bus)
        logger.create_fahrstrasse(event)
        log_entry = (
            CreateFahrstrasseLogEntry.select()
            .where(
                (CreateFahrstrasseLogEntry.tick == tick)
                & (CreateFahrstrasseLogEntry.fahrstrasse == fahrstrasse)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Fahrstrasse {fahrstrasse} created"
        assert log_entry.run_id.id == run.id
        assert log_entry.fahrstrasse == fahrstrasse

    @freeze_time()
    def test_remove_fahrstrasse(self, run, tick, fahrstrasse, event_bus):
        event = Event(
            EventType.REMOVE_FAHRSTRASSE, {"tick": tick, "fahrstrasse": fahrstrasse}
        )
        logger = Logger(event_bus=event_bus)
        logger.remove_fahrstrasse(event)
        log_entry = (
            RemoveFahrstrasseLogEntry.select()
            .where(
                (RemoveFahrstrasseLogEntry.tick == tick)
                & (RemoveFahrstrasseLogEntry.fahrstrasse == fahrstrasse)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert log_entry.message == f"Fahrstrasse {fahrstrasse} removed"
        assert log_entry.run_id.id == run.id
        assert log_entry.fahrstrasse == fahrstrasse

    @freeze_time()
    def test_set_signal(
        self, run, tick, signal_id, state_before, state_after, event_bus
    ):
        event = Event(
            EventType.SET_SIGNAL,
            {
                "tick": tick,
                "signal_id": signal_id,
                "state_before": state_before,
                "state_after": state_after,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.set_signal(event)
        log_entry = (
            SetSignalLogEntry.select()
            .where(
                (SetSignalLogEntry.tick == tick)
                & (SetSignalLogEntry.signal_id == signal_id)
                & (SetSignalLogEntry.state_before == state_before)
                & (SetSignalLogEntry.state_after == state_after)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Signal with ID {signal_id} changed from {state_before} to {state_after}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.signal_id == signal_id
        assert log_entry.state_before == state_before
        assert log_entry.state_after == state_after

    @freeze_time()
    def test_train_enter_block_section(
        self, run, tick, train_id, block_section_id, block_section_length, event_bus
    ):
        event = Event(
            EventType.TRAIN_ENTER_BLOCK_SECTION,
            {
                "tick": tick,
                "train_id": train_id,
                "block_section_id": block_section_id,
                "block_section_length": block_section_length,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.train_enter_block_section(event)
        log_entry = (
            TrainEnterBlockSectionLogEntry.select()
            .where(
                (TrainEnterBlockSectionLogEntry.tick == tick)
                & (TrainEnterBlockSectionLogEntry.train_id == train_id)
                & (TrainEnterBlockSectionLogEntry.block_section_id == block_section_id)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train with ID {train_id} entered block section with ID {block_section_id} with "
            f"length {block_section_length}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
        assert log_entry.block_section_id == block_section_id
        assert log_entry.block_section_length == block_section_length

    @freeze_time()
    def test_train_leave_block_section(
        self, run, tick, train_id, block_section_id, block_section_length, event_bus
    ):
        event = Event(
            EventType.TRAIN_LEAVE_BLOCK_SECTION,
            {
                "tick": tick,
                "train_id": train_id,
                "block_section_id": block_section_id,
                "block_section_length": block_section_length,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.train_leave_block_section(event)
        log_entry = (
            TrainLeaveBlockSectionLogEntry.select()
            .where(
                (TrainLeaveBlockSectionLogEntry.tick == tick)
                & (TrainLeaveBlockSectionLogEntry.train_id == train_id)
                & (TrainLeaveBlockSectionLogEntry.block_section_id == block_section_id)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train with ID {train_id} left block section with ID {block_section_id}"
        )
        assert log_entry.run_id.id == run.id
        assert log_entry.train_id == train_id
        assert log_entry.block_section_id == block_section_id

    @freeze_time()
    def test_inject_platform_blocked_fault(
        self,
        run,
        tick,
        platform_blocked_fault_configuration,
        affected_element,
        event_bus,
    ):
        event = Event(
            EventType.INJECT_FAULT,
            {
                "tick": tick,
                "platform_blocked_fault_configuration": platform_blocked_fault_configuration,
                "affected_element": affected_element,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.inject_platform_blocked_fault(event)
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                (InjectFaultLogEntry.tick == tick)
                & (
                    InjectFaultLogEntry.platform_blocked_fault_configuration
                    == platform_blocked_fault_configuration
                )
                & (InjectFaultLogEntry.affected_element == affected_element)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Platform blocked fault with configuration {platform_blocked_fault_configuration} "
            f"on element {affected_element}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.platform_blocked_fault_configuration
            == platform_blocked_fault_configuration
        )
        assert log_entry.affected_element == affected_element

        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_track_blocked_fault(
        self, run, tick, track_blocked_fault_configuration, affected_element, event_bus
    ):
        event = Event(
            EventType.INJECT_FAULT,
            {
                "tick": tick,
                "track_blocked_fault_configuration": track_blocked_fault_configuration,
                "affected_element": affected_element,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.inject_track_blocked_fault(event)
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                (InjectFaultLogEntry.tick == tick)
                & (
                    InjectFaultLogEntry.track_blocked_fault_configuration
                    == track_blocked_fault_configuration
                )
                & (InjectFaultLogEntry.affected_element == affected_element)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Track blocked fault with configuration {track_blocked_fault_configuration} "
            f"on element {affected_element}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.track_blocked_fault_configuration
            == track_blocked_fault_configuration
        )
        assert log_entry.affected_element == affected_element

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_track_speed_limit_fault(
        self,
        run,
        tick,
        track_speed_limit_fault_configuration,
        affected_element,
        value_before,
        value_after,
        event_bus,
    ):
        event = Event(
            EventType.INJECT_FAULT,
            {
                "tick": tick,
                "track_speed_limit_fault_configuration": track_speed_limit_fault_configuration,
                "affected_element": affected_element,
                "value_before": value_before,
                "value_after": value_after,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.inject_track_speed_limit_fault(event)
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                (InjectFaultLogEntry.tick == tick)
                & (
                    InjectFaultLogEntry.track_speed_limit_fault_configuration
                    == track_speed_limit_fault_configuration
                )
                & (InjectFaultLogEntry.affected_element == affected_element)
                & (InjectFaultLogEntry.value_before == value_before)
                & (InjectFaultLogEntry.value_after == value_after)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message == f"Track speed limit fault with configuration "
            f"{track_speed_limit_fault_configuration} on element {affected_element} changed "
            f"from {value_before} to {value_after}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.track_speed_limit_fault_configuration
            == track_speed_limit_fault_configuration
        )
        assert log_entry.affected_element == affected_element
        assert log_entry.value_before == value_before
        assert log_entry.value_after == value_after

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_schedule_blocked_fault(
        self,
        run,
        tick,
        schedule_blocked_fault_configuration,
        affected_element,
        event_bus,
    ):
        event = Event(
            EventType.INJECT_FAULT,
            {
                "tick": tick,
                "schedule_blocked_fault_configuration": schedule_blocked_fault_configuration,
                "affected_element": affected_element,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.inject_schedule_blocked_fault(event)
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                (InjectFaultLogEntry.tick == tick)
                & (
                    InjectFaultLogEntry.schedule_blocked_fault_configuration
                    == schedule_blocked_fault_configuration
                )
                & (InjectFaultLogEntry.affected_element == affected_element)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Schedule blocked fault with configuration {schedule_blocked_fault_configuration} "
            f"on element {affected_element}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.schedule_blocked_fault_configuration
            == schedule_blocked_fault_configuration
        )
        assert log_entry.affected_element == affected_element

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_train_prio_fault(
        self,
        run,
        tick,
        train_prio_fault_configuration,
        affected_element,
        value_before,
        value_after,
        event_bus,
    ):
        event = Event(
            EventType.INJECT_FAULT,
            {
                "tick": tick,
                "train_prio_fault_configuration": train_prio_fault_configuration,
                "affected_element": affected_element,
                "value_before": value_before,
                "value_after": value_after,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.inject_train_prio_fault(event)
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                (InjectFaultLogEntry.tick == tick)
                & (
                    InjectFaultLogEntry.train_prio_fault_configuration
                    == train_prio_fault_configuration
                )
                & (InjectFaultLogEntry.affected_element == affected_element)
                & (InjectFaultLogEntry.value_before == value_before)
                & (InjectFaultLogEntry.value_after == value_after)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train prio fault with configuration {train_prio_fault_configuration} "
            f"on element {affected_element} changed from {value_before} to {value_after}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.train_prio_fault_configuration == train_prio_fault_configuration
        )
        assert log_entry.affected_element == affected_element
        assert log_entry.value_before == value_before
        assert log_entry.value_after == value_after

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_inject_train_speed_fault(
        self,
        run,
        tick,
        train_speed_fault_configuration,
        affected_element,
        value_before,
        value_after,
        event_bus,
    ):
        event = Event(
            EventType.INJECT_FAULT,
            {
                "tick": tick,
                "train_speed_fault_configuration": train_speed_fault_configuration,
                "affected_element": affected_element,
                "value_before": value_before,
                "value_after": value_after,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.inject_train_speed_fault(event)
        log_entry = (
            InjectFaultLogEntry.select()
            .where(
                (InjectFaultLogEntry.tick == tick)
                & (
                    InjectFaultLogEntry.train_speed_fault_configuration
                    == train_speed_fault_configuration
                )
                & (InjectFaultLogEntry.affected_element == affected_element)
                & (InjectFaultLogEntry.value_before == value_before)
                & (InjectFaultLogEntry.value_after == value_after)
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train speed fault with configuration {train_speed_fault_configuration} "
            f"on element {affected_element} changed from {value_before} to {value_after}"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.train_speed_fault_configuration == train_speed_fault_configuration
        )
        assert log_entry.affected_element == affected_element
        assert log_entry.value_before == value_before
        assert log_entry.value_after == value_after

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None

    @freeze_time()
    def test_resolve_platform_blocked_fault(
        self, run, tick, platform_blocked_fault_configuration, event_bus
    ):
        event = Event(
            EventType.RESOLVE_FAULT,
            {
                "tick": tick,
                "platform_blocked_fault_configuration": platform_blocked_fault_configuration,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.resolve_platform_blocked_fault(event)
        log_entry = (
            ResolveFaultLogEntry.select()
            .where(
                (ResolveFaultLogEntry.tick == tick)
                & (
                    ResolveFaultLogEntry.platform_blocked_fault_configuration
                    == platform_blocked_fault_configuration
                )
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Platform blocked fault with configuration {platform_blocked_fault_configuration} "
            f"resolved"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.platform_blocked_fault_configuration
            == platform_blocked_fault_configuration
        )

        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_resolve_track_blocked_fault(
        self, run, tick, track_blocked_fault_configuration, event_bus
    ):
        event = Event(
            EventType.RESOLVE_FAULT,
            {
                "tick": tick,
                "track_blocked_fault_configuration": track_blocked_fault_configuration,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.resolve_track_blocked_fault(event)
        log_entry = (
            ResolveFaultLogEntry.select()
            .where(
                (ResolveFaultLogEntry.tick == tick)
                & (
                    ResolveFaultLogEntry.track_blocked_fault_configuration
                    == track_blocked_fault_configuration
                )
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Track blocked fault with configuration {track_blocked_fault_configuration} "
            f"resolved"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.track_blocked_fault_configuration
            == track_blocked_fault_configuration
        )

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_resolve_track_speed_limit_fault(
        self, run, tick, track_speed_limit_fault_configuration, event_bus
    ):
        event = Event(
            EventType.RESOLVE_FAULT,
            {
                "tick": tick,
                "track_speed_limit_fault_configuration": track_speed_limit_fault_configuration,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.resolve_track_speed_limit_fault(event)
        log_entry = (
            ResolveFaultLogEntry.select()
            .where(
                (ResolveFaultLogEntry.tick == tick)
                & (
                    ResolveFaultLogEntry.track_speed_limit_fault_configuration
                    == track_speed_limit_fault_configuration
                )
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message == f"Track speed limit fault with configuration "
            f"{track_speed_limit_fault_configuration} resolved"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.track_speed_limit_fault_configuration
            == track_speed_limit_fault_configuration
        )

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_resolve_schedule_blocked_fault(
        self, run, tick, schedule_blocked_fault_configuration, event_bus
    ):
        event = Event(
            EventType.RESOLVE_FAULT,
            {
                "tick": tick,
                "schedule_blocked_fault_configuration": schedule_blocked_fault_configuration,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.resolve_schedule_blocked_fault(event)
        log_entry = (
            ResolveFaultLogEntry.select()
            .where(
                (ResolveFaultLogEntry.tick == tick)
                & (
                    ResolveFaultLogEntry.schedule_blocked_fault_configuration
                    == schedule_blocked_fault_configuration
                )
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Schedule blocked fault with configuration {schedule_blocked_fault_configuration} "
            f"resolved"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.schedule_blocked_fault_configuration
            == schedule_blocked_fault_configuration
        )

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_resolve_train_prio_fault(
        self, run, tick, train_prio_fault_configuration, event_bus
    ):
        event = Event(
            EventType.RESOLVE_FAULT,
            {
                "tick": tick,
                "train_prio_fault_configuration": train_prio_fault_configuration,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.resolve_train_prio_fault(event)
        log_entry = (
            ResolveFaultLogEntry.select()
            .where(
                (ResolveFaultLogEntry.tick == tick)
                & (
                    ResolveFaultLogEntry.train_prio_fault_configuration
                    == train_prio_fault_configuration
                )
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train prio fault with configuration {train_prio_fault_configuration} "
            f"resolved"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.train_prio_fault_configuration == train_prio_fault_configuration
        )

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_speed_fault_configuration is None

    @freeze_time()
    def test_resolve_train_speed_fault(
        self, run, tick, train_speed_fault_configuration, event_bus
    ):
        event = Event(
            EventType.RESOLVE_FAULT,
            {
                "tick": tick,
                "train_speed_fault_configuration": train_speed_fault_configuration,
            },
        )
        logger = Logger(event_bus=event_bus)
        logger.resolve_train_speed_fault(event)
        log_entry = (
            ResolveFaultLogEntry.select()
            .where(
                (ResolveFaultLogEntry.tick == tick)
                & (
                    ResolveFaultLogEntry.train_speed_fault_configuration
                    == train_speed_fault_configuration
                )
            )
            .first()
        )
        assert log_entry.timestamp == datetime.now()
        assert log_entry.tick == tick
        assert (
            log_entry.message
            == f"Train speed fault with configuration {train_speed_fault_configuration} "
            f"resolved"
        )
        assert log_entry.run_id.id == run.id
        assert (
            log_entry.train_speed_fault_configuration == train_speed_fault_configuration
        )

        assert log_entry.platform_blocked_fault_configuration is None
        assert log_entry.track_blocked_fault_configuration is None
        assert log_entry.track_speed_limit_fault_configuration is None
        assert log_entry.schedule_blocked_fault_configuration is None
        assert log_entry.train_prio_fault_configuration is None
