"""
This module contains the logger class
"""
from datetime import datetime
from typing import Type
from uuid import UUID

from src.logger.log_entry import (
    RemoveFahrstrasseLogEntry,
    TrainRemoveLogEntry,
    TrainSpawnLogEntry,
)


class Logger:
    """
    The logger class is used to log the events of the simulation
    """

    run_id: int

    def __init__(self, run_id: int):
        """
        The constructor of the logger class
        """
        self.run_id = run_id

    def spawn_train(self, tick: int, train_id: str) -> Type[None]:
        """
        This function should be called when a train is being spawned. This should include a train
        identifier.
        :param tick: The current simulation tick
        :param train_id: The id of the train
        :rtype: None
        """
        TrainSpawnLogEntry.create(
            timestamp=datetime.now(),
            tick=tick,
            message=f"Train with ID {train_id} spawned",
            run_id=self.run_id,
            train_id=train_id,
        )

    def remove_train(self, tick: int, train_id: str) -> Type[None]:
        """
        This function should be called when a train is being removed. This should include a train
        identifier.
        :param tick: The current simulation tick
        :param train_id: The id of the train
        :rtype: None
        """
        TrainRemoveLogEntry.create(
            timestamp=datetime.now(),
            tick=tick,
            message=f"Train with ID {train_id} removed",
            run_id=self.run_id,
            train_id=train_id,
        )

    def arrival_train(self, tick: int, train_id: str, station_id: str) -> Type[None]:
        """
        This function should be called when a train arrives at a station. This should include a
        train identifier and the station identifier.
        :param tick: The current simulation tick
        :param train_id: The id of the train
        :param station_id: The id of the station
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def departure_train(self, tick: int, train_id: str, station_id: str) -> Type[None]:
        """
        This function should be called when a train departs from a station. This should include a
        train identifier and the station identifier.
        :param tick: The current simulation tick
        :param train_id: The id of the train
        :param station_id: The id of the station
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def create_fahrstrasse(self, tick: int, fahrstrasse: str) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is being formed. This should include the
        definition of the Fahrstrasse.
        :param tick: The current simulation tick
        :param fahrstrasse: The definition of the created fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def remove_fahrstrasse(self, tick: int, fahrstrasse: str) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is being dissolved. This should include
        the definition of the Fahrstrasse.
        :param tick: The current simulation tick
        :param fahrstrasse: The definition of the removed fahrstrasse
        :rtype: None
        """
        RemoveFahrstrasseLogEntry.create(
            timestamp=datetime.now(),
            tick=tick,
            message=f"Fahrstrasse {fahrstrasse} removed",
            run_id=self.run_id,
            fahrstrasse=fahrstrasse,
        )

    def set_signal(
        self, tick: int, signal_id: UUID, state_before: int, state_after: int
    ) -> Type[None]:
        """
        This function is being called when setting a signal or changing its state. This should
        include the signal identifier, the state before and the state after the change.
        :param tick: The current simulation tick
        :param signal_id: The id of the signal
        :param state_before: The state of the signal before the change
        :param state_after: The state of the signal after the change
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    # pylint: disable=too-many-arguments
    def inject_platform_blocked_fault(
        self,
        tick: int,
        platform_blocked_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a platform blocked fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param tick: The current simulation tick
        :param platform_blocked_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    # pylint: disable=too-many-arguments
    def inject_track_blocked_fault(
        self,
        tick: int,
        track_blocked_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a track blocked fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param tick: The current simulation tick
        :param track_blocked_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    # pylint: disable=too-many-arguments
    def inject_track_speed_limit_fault(
        self,
        tick: int,
        track_speed_limit_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a track speed limit fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param tick: The current simulation tick
        :param track_speed_limit_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    # pylint: disable=too-many-arguments
    def inject_train_cancelled_speed_fault(
        self,
        tick: int,
        train_cancelled_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a train speed fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param tick: The current simulation tick
        :param train_cancelled_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    # pylint: disable=too-many-arguments
    def inject_train_prio_fault_configuration(
        self,
        tick: int,
        train_prio_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a train prio fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param tick: The current simulation tick
        :param train_prio_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    # pylint: disable=too-many-arguments
    def inject_train_speed_fault(
        self,
        tick: int,
        train_speed_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a train speed fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param tick: The current simulation tick
        :param train_speed_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_platform_blocked_fault(
        self, tick: int, platform_blocked_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a platform blocked fault from the simulation.
        This should reference the fault configuration of the fault.
        :param tick: The current simulation tick
        :param platform_blocked_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_track_blocked_fault(
        self, tick: int, track_blocked_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a track blocked fault from the simulation.
        This should reference the fault configuration of the fault.
        :param tick: The current simulation tick
        :param track_blocked_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_track_speed_limit_fault(
        self, tick: int, track_speed_limit_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a track speed limit fault from the simulation.
        This should reference the fault configuration of the fault.
        :param tick: The current simulation tick
        :param track_speed_limit_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_train_cancelled_fault(
        self, tick: int, train_cancelled_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a train cancelled fault from the simulation.
        This should reference the fault configuration of the fault.
        :param tick: The current simulation tick
        :param train_cancelled_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_train_prio_fault_configuration(
        self, tick: int, train_prio_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a train prio fault from the simulation.
        This should reference the fault configuration of the fault.
        :param tick: The current simulation tick
        :param train_prio_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_train_speed_fault(
        self, tick: int, train_speed_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a train speed fault from the simulation. This
        should reference the fault configuration of the fault.
        :param tick: The current simulation tick
        :param train_speed_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107
