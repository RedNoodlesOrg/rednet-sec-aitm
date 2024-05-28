from __future__ import annotations

from simple_observer.event import Event


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
