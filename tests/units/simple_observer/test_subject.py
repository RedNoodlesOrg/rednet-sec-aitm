from __future__ import annotations

import unittest

from simple_observer.observer import Observer
from simple_observer.subject import Subject


class MockObserver(Observer):
    def __init__(self):
        super().__init__()
        self.updated = False

    def update(self, *args, **kwargs):
        self.updated = True


class MockSubject(Subject):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update()


class TestSubject(unittest.TestCase):

    def setUp(self):
        self.subject = MockSubject()
        self.observer = MockObserver()

    def test_register_observer(self):
        self.subject.attach(self.observer)
        self.assertIn(self.observer, self.subject._observers)

    def test_unregister_observer(self):
        self.subject.attach(self.observer)
        self.subject.detach(self.observer)
        self.subject.notify()
        self.assertFalse(self.observer.updated)

    def test_notify_observers(self):
        self.subject.attach(self.observer)
        self.subject.notify()
        self.assertTrue(self.observer.updated)


if __name__ == "__main__":
    unittest.main()
