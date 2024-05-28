from __future__ import annotations

from simple_observer.event import Event


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
