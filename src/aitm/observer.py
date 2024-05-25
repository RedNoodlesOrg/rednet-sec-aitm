from __future__ import annotations

import asyncio
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


class Event:
    """
    Represents an event in the system.

    Attributes:
        event_type (str): The type of the event.
        data (Any): Optional data associated with the event.
    """

    __slots__ = ["event_type", "data"]

    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data


class CredentialsCapturedEvent(Event):
    """
    Represents an event that is triggered when credentials are captured.

    Attributes:
        username (str): The captured username.
        password (str): The captured password.
    """

    def __init__(self, username: str, password: str):
        super().__init__("CredentialsCapturedEvent", {"username": username, "password": password})
        self.username = username
        self.password = password


class MfaSessionCapturedEvent(Event):
    """
    Represents an event when an MFA session is captured.

    Attributes:
        parsed_cookies (list[dict[str, str]]): A list of dictionaries representing parsed cookies.
        user_agent (str): The user agent string associated with the event.
    """

    def __init__(self, parsed_cookies: list[dict[str, str]], user_agent: str):
        super().__init__("MfaSessionCapturedEvent", {"parsed_cookies": parsed_cookies, "user_agent": user_agent})
        self.parsed_cookies = parsed_cookies
        self.user_agent = user_agent


class EventEmitter:
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
        self._observers = []

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
