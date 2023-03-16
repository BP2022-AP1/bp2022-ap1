from abc import ABC, abstractmethod


class Component(ABC):

    @abstractmethod
    def nextTick(self, tick: int):
        raise NotImplementedError()
