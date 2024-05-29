from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from aitm.events.listener import EventListener
from simple_observer import Event, Subject


class MockSubject(Subject):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(self, event)


class TestEventListener(unittest.TestCase):

    def setUp(self):
        self.subject = MockSubject()
        self.listener = EventListener()

    def test_update(self):
        event = Event("test_event", {"data": "test_data"})
        self.listener.update = MagicMock()
        self.subject.attach(self.listener)
        self.subject.notify(event)
        self.listener.update.assert_called_once_with(self.subject, event)


if __name__ == "__main__":
    unittest.main()
