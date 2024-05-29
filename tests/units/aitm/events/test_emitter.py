from __future__ import annotations

import asyncio
import unittest

from aitm.events.emitter import EventEmitter
from simple_observer import Event, Observer


class MockObserver(Observer):
    def __init__(self):
        super().__init__()
        self.updated = False

    async def update(self, subject, event):
        self.updated = True


class TestEventEmitter(unittest.TestCase):

    def setUp(self):
        self.emitter = EventEmitter()
        self.observer = MockObserver()

    def test_attach_observer(self):
        self.emitter.attach(self.observer)
        self.assertIn(self.observer, self.emitter._observers)

    def test_detach_observer(self):
        self.emitter.attach(self.observer)
        self.emitter.detach(self.observer)
        self.assertNotIn(self.observer, self.emitter._observers)

    def test_detach_nonexistent_observer(self):
        observer = MockObserver()
        self.emitter.detach(observer)  # Should not raise an exception

    def test_notify_no_observers(self):
        event = Event("test")
        self.emitter.notify(event)  # Should not raise an exception


class TestEventEmitterAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.emitter = EventEmitter()
        self.observer = MockObserver()

    def test_attach_observer(self):
        self.emitter.attach(self.observer)
        self.assertIn(self.observer, self.emitter._observers)

    async def test_notify_observers(self):
        event = Event(event_type="test")
        self.emitter.attach(self.observer)
        self.emitter.notify(event)
        await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
        self.assertTrue(self.observer.updated)

    async def test_notify_multiple_observers(self):
        event = Event("test")
        observer1 = MockObserver()
        observer2 = MockObserver()
        self.emitter.attach(observer1)
        self.emitter.attach(observer2)
        self.emitter.notify(event)
        await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
        self.assertTrue(observer1.updated)
        self.assertTrue(observer2.updated)


if __name__ == "__main__":
    unittest.main()
