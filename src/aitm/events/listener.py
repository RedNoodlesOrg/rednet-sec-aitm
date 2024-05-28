from __future__ import annotations

from simple_observer import Event, Observer, Subject


class EventListener(Observer):
    """
    A class that represents an event listener.

    An event listener is an observer that listens for events emitted by an event emitter.

    Attributes:
        _subject (EventEmitter): The event emitter to listen to.

    Methods:
        update(subject, event): Updates the event listener with a new event.
    """

    async def update(self, subject: Subject, event: Event) -> None:
        """
        Updates the event listener with a new event.

        Args:
            subject (EventEmitter): The subject that triggered the event.
            event: The event that occurred.

        Returns:
            None
        """
        print(f"Event listener received event: {event}")
