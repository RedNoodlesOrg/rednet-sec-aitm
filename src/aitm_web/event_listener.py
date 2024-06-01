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

    history: list[Event]
    _singelton = None

    def __init__(self):
        self.history = []

    async def update(self, subject: Subject, event: Event) -> None:
        """
        Updates the event listener with a new event.

        Args:
            subject (EventEmitter): The subject that triggered the event.
            event: The event that occurred.

        Returns:
            None
        """
        self.history.append(event)
        print(f"Event listener received event: {event}")

    @staticmethod
    def get_listener() -> EventListener:
        """
        Returns the singleton instance of the EventListener class.

        If the singleton instance does not exist, it creates a new instance and returns it.

        Returns:
            EventListener: The singleton instance of the EventListener class.
        """
        if EventListener._singelton is None:
            EventListener._singelton = EventListener()
        return EventListener._singelton
