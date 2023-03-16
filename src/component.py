from abc import ABC, abstractmethod


class Component(ABC):

    @abstractmethod
    def nextTick(self, tick: int):
        """
        Called to announce that the next tick occurred.
        :param tick: The current tick.
        :rtype: None
        """
        raise NotImplementedError()
