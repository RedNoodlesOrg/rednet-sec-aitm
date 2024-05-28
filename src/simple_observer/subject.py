from __future__ import annotations

from abc import ABC, abstractmethod


class Subject(ABC):
    def __init__(self):
        self._observers = []

    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self, event):
        pass
