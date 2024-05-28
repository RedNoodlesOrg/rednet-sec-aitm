from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    """
    The base class for all observers.

    Observers are objects that receive updates from a subject when its state changes.
    To create a custom observer, subclass this class and implement the `update` method.
    """

    @abstractmethod
    async def update(self, subject, event):
        """
        This method is called when the observer needs to be updated with a new event.

        Args:
            subject: The subject that triggered the event.
            event: The event that occurred.
        """
        pass
