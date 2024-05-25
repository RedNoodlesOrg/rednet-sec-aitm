from __future__ import annotations

import asyncio

import pytest

from aitm.observer import Event, EventEmitter, Observer


class TestObserver(Observer):
    async def update(self, subject, event):
        pass


def test_attach():
    emitter = EventEmitter()
    observer = TestObserver()
    emitter.attach(observer)
    assert observer in emitter._observers


def test_detach():
    emitter = EventEmitter()
    observer = TestObserver()
    emitter.attach(observer)
    emitter.detach(observer)
    assert observer not in emitter._observers


@pytest.mark.asyncio
async def test_notify_async():
    class TestObserver(Observer):
        def __init__(self):
            self.updated = False

        async def update(self, subject, event):
            self.updated = True

    emitter = EventEmitter()
    observer = TestObserver()
    emitter.attach(observer)
    event = Event("TestEvent")
    emitter.notify(event)
    await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
    assert observer.updated


@pytest.mark.asyncio
async def test_notify_multiple_observers():
    class TestObserver1(Observer):
        def __init__(self):
            self.updated = False

        async def update(self, subject, event):
            await asyncio.sleep(1)  # Simulate some async work
            self.updated = True

    class TestObserver2(Observer):
        def __init__(self):
            self.updated = False

        async def update(self, subject, event):
            await asyncio.sleep(5)  # Simulate some async work
            self.updated = True

    emitter = EventEmitter()
    observer1 = TestObserver1()
    observer2 = TestObserver2()
    emitter.attach(observer1)
    emitter.attach(observer2)
    event = Event("TestEvent")
    emitter.notify(event)
    await asyncio.gather(*asyncio.all_tasks() - {asyncio.current_task()})
    assert observer1.updated
    assert observer2.updated
