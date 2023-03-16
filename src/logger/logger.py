"""
This module contains the logger class
"""
from typing import Type


class Logger:
    """
    The logger class is used to log the events of the simulation

    :ivar connection_string: str
    """

    def __init__(self, connection_string):
        self.connection_string = connection_string

    def spawn_train(self, train_id: int) -> Type[None]:
        """
        This function should be called when a train is beeing spawned. This should include a train
        identifier, the type of train, the route (if not specified by schedule), and the position.
        :param train_id: The id of the train
        :rtype: None
        """
        pass  # not implemented yet

    def remove_train(self, train_id: int) -> Type[None]:
        """
        This function should be called when a train is beeing removed. This should include a train
        identifier, the type of train, and the position.
        :param train_id: The id of the train
        :rtype: None
        """
        pass  # not implemented yet

    def arrival_train(self, train_id: int, station_id: int) -> Type[None]:
        """
        This function should be called when a train arrives at a station. This should include a
        train identifier, the type of train, and the station identifier, maybe platform (?).
        :param train_id: The id of the train
        :param station_id: The id of the station
        :rtype: None
        """
        pass  # not implemented yet

    def departure_train(self, train_id: int, station_id: int) -> Type[None]:
        """
        This function should be called when a train departes from a station. This should include a
        train identifier, the type of train, and the station identifier, maybe platform (?).
                :param train_id: The id of the train
                :param station_id: The id of the station
                :rtype: None
        """
        pass  # not implemented yet

    def create_fahrstrasse(self, fahrstrasse: any) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is beeing formed. This should include the
        definition of the Fahrstrasse.
        :param fahrstrasse: The definition of the created fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet

    def remove_fahrstrasse(self, fahrstrasse: any) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is beeing dissolved. This should include
        the definition of the Fahrstrasse.
        :param fahrstrasse: The definition of the removed fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet

    def set_signal(
        self, signal_id: int, state_before: int, state_after: int
    ) -> Type[None]:
        """
        This function is beeing called when setting a signal or changing its state. This should
        include the signal identifier, the state before and the state after the change.
        :param signal_id: The id of the signal
        :param state_before: The state of the signal before the change
        :param state_after: The state of the signal after the change
        :rtype: None
        """
        pass  # not implemented yet

    def inject_fault(
        self, injection_id: int, fault_type: int, injection_position: any, duration: int
    ) -> Type[None]:
        """
        This function should be called when injecting a fault into the simulation. This should
        include (the injection id), type of injection, position of injection, duration and some
        information if required. (Maybe adapt later)
        :param injection_id: The id of the injection
        :param fault_type: The fault type
        :param injection_position: The position of the injection
        :param duration: The duration of the injection
        :rtype: None
        """
        pass  # not implemented yet

    def remove_fault(self, injection_id: int) -> Type[None]:
        """
        This function should be called when removing a fault from the simulation. This should
        reference the injection id, that was removed.
        :param injection_id: The id of the injection
        :rtype: None
        """
        pass  # not implemented yet
