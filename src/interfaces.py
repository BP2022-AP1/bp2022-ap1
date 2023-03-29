# pylint: disable=C0115, C0116

from collections.abc import Callable
from typing import Protocol


class IInfrastructureProvider(Protocol):
    """Provides the api for the interlocking component to control the simulation"""

    def turn_point(self, yaramo_point: str, target_orientation: str) -> None:
        """Changes the specified switch to the given orientation

        :param yaramo_point: The yarmo-id of the switch which is getting turned
        :param target_orientation: The target orientation, one of 'left', 'right'
        """

    def set_signal_state(self, yaramo_signal: str, target_state: str) -> None:
        """Changes the signal to the given state

        :param yaramo_signal: The yaramo-id of the signal which is getting updated
        :param target_state: The target state, one of 'halt', 'go'
        """

    def tds_count_in_callback(self, callback: Callable[[str], None]) -> None:
        """Updates the callback which is called when a train enters a specific track segment

        :param callback: The callback which takes an yaramo-track-id as an input and returns nothing
        """

    def tds_count_out_callback(self, callback: Callable[[str], None]) -> None:
        """Updates the callback which is called when a train exits a specific track segment

        :param callback: The callback which takes an yaramo-track-id as an input and returns nothing
        """


class ISpawnerRestrictor(Protocol):
    def block_schedule(self, schedule_id: int):
        ...

    def unblock_schedule(self, schedule_id: int):
        ...
