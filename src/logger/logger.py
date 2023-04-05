"""
This module contains the logger class
"""
from datetime import datetime
from typing import Type

from src.logger.log_entry import TrainSpawnLogEntry


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

    def spawn_train(self, train_id: int) -> Type[None]:
        """
        This function should be called when a train is beeing spawned. This should include a train
        identifier, the type of train, the route (if not specified by schedule), and the position.
        :param train_id: The id of the train
        :rtype: None
        """
        spawn_train_log_entry = TrainSpawnLogEntry.create(
            timestamp=datetime.now(),
            message=f"Train with ID {train_id} spawned",
            run_id=self.run_id,
            train_id=train_id,
        )
        spawn_train_log_entry.save()

    def remove_train(self, train_id: int) -> Type[None]:
        """
        This function should be called when a train is beeing removed. This should include a train
        identifier, the type of train, and the position.
        :param train_id: The id of the train
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def arrival_train(self, train_id: int, station_id: int) -> Type[None]:
        """
        This function should be called when a train arrives at a station. This should include a
        train identifier, the type of train, and the station identifier, maybe platform (?).
        :param train_id: The id of the train
        :param station_id: The id of the station
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def departure_train(self, train_id: int, station_id: int) -> Type[None]:
        """
        This function should be called when a train departes from a station. This should include a
        train identifier, the type of train, and the station identifier, maybe platform (?).
                :param train_id: The id of the train
                :param station_id: The id of the station
                :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def create_fahrstrasse(self, fahrstrasse: any) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is beeing formed. This should include the
        definition of the Fahrstrasse.
        :param fahrstrasse: The definition of the created fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

    def remove_fahrstrasse(self, fahrstrasse: any) -> Type[None]:
        """
        This function should be called when a Fahrstrasse is beeing dissolved. This should include
        the definition of the Fahrstrasse.
        :param fahrstrasse: The definition of the removed fahrstrasse
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107

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
        pass  # not implemented yet # pylint: disable=W0107

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
        pass  # not implemented yet # pylint: disable=W0107

    def remove_fault(self, injection_id: int) -> Type[None]:
        """
        This function should be called when removing a fault from the simulation. This should
        reference the injection id, that was removed.
        :param injection_id: The id of the injection
        :rtype: None
        """
        pass  # not implemented yet # pylint: disable=W0107
