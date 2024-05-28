from __future__ import annotations

from abc import ABC, abstractmethod


class Subject(ABC):
    def __init__(self):
        self._observers = []

    @abstractmethod
    def attach(self, observer):
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer):
        raise NotImplementedError

    @abstractmethod
    def notify(self, event):
        raise NotImplementedError
