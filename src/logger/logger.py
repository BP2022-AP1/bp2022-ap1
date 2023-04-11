"""
This module contains the logger class
"""
from typing import Type
from uuid import UUID


class Logger:
    """
    The logger class is used to log the events of the simulation
    """

    def spawn_train(self, train_id: str) -> Type[None]:
        """
        This function should be called when a train is being spawned. This should include a train
        identifier.
        :param train_id: The id of the train
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def remove_train(self, train_id: str) -> Type[None]:
        """
        This function should be called when a train is being removed. This should include a train
        identifier.
        :param train_id: The id of the train
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def arrival_train(self, train_id: str, station_id: str) -> Type[None]:
        """
        This function should be called when a train arrives at a station. This should include a
        train identifier and the station identifier.
        :param train_id: The id of the train
        :param station_id: The id of the station
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def departure_train(self, train_id: str, station_id: str) -> Type[None]:
        """
        This function should be called when a train departs from a station. This should include a
        train identifier and the station identifier.
                :param train_id: The id of the train
                :param station_id: The id of the station
                :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def create_fahrstrasse(self, fahrstrasse: str) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is being formed. This should include the
        definition of the Fahrstrasse.
        :param fahrstrasse: The definition of the created fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def remove_fahrstrasse(self, fahrstrasse: str) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is being dissolved. This should include
        the definition of the Fahrstrasse.
        :param fahrstrasse: The definition of the removed fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def set_signal(
        self, signal_id: UUID, state_before: int, state_after: int
    ) -> Type[None]:
        """
        This function is being called when setting a signal or changing its state. This should
        include the signal identifier, the state before and the state after the change.
        :param signal_id: The id of the signal
        :param state_before: The state of the signal before the change
        :param state_after: The state of the signal after the change
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def inject_train_speed_fault(
        self,
        train_speed_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a train speed fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param train_speed_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def inject_platform_blocked_fault(
        self,
        platform_blocked_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a platform blocked fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param platform_blocked_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """

    pass  # not implemented yet # pylint: disable=W0107

    def inject_train_cancelled_speed_fault(
        self,
        train_cancelled_fault_configuration: UUID,
        affected_element: str,
        value_before: str,
        value_after: str,
    ) -> Type[None]:
        """
        This function should be called when injecting a train speed fault into the simulation.
        This should include the fault configuration, the affected element, the value before and the
        value after the fault.
        :param train_cancelled_fault_configuration: The configuration of the fault
        :param affected_element: The affected element
        :param value_before: The value before the fault
        :param value_after: The value after the fault
        :rtype: None
        """

    pass  # not implemented yet # pylint: disable=W0107

    def resolve_train_speed_fault(
        self, train_speed_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a train speed fault from the simulation. This
        should reference the fault configuration of the fault.
        :param train_speed_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_platform_blocked_fault(
        self, platform_blocked_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a platform blocked fault from the simulation.
        This should reference the fault configuration of the fault.
        :param platform_blocked_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def resolve_train_cancelled_fault(
        self, train_cancelled_fault_configuration: UUID
    ) -> Type[None]:
        """
        This function should be called when removing a train cancelled fault from the simulation.
        This should reference the fault configuration of the fault.
        :param train_cancelled_fault_configuration: The configuration of the fault
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107
