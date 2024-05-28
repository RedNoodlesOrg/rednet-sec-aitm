from __future__ import annotations

import asyncio

from simple_observer import Subject


class EventEmitter(Subject):
    """
    A class that represents an event emitter.

    An event emitter allows attaching, detaching, and notifying observers.

    Attributes:
        _observers (list): A list of observers attached to the event emitter.

    Methods:
        attach(observer): Attaches an observer to the event emitter.
        detach(observer): Detaches an observer from the event emitter.
        notify(event): Notifies all attached observers with the given event.
    """

    def __init__(self):
        super().__init__()

    def attach(self, observer):
        """
        Attaches an observer to the event emitter.

        Args:
            observer: The observer to attach.

        Returns:
            None
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Detaches an observer from the event emitter.

        Args:
            observer: The observer to detach.

        Returns:
            None
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event):
        """
        Notifies all attached observers with the given event.

        Args:
            event: The event to notify the observers with.

        Returns:
            None
        """
        for observer in self._observers:
            asyncio.create_task(observer.update(self, event))
