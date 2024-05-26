from __future__ import annotations

from enum import Enum

import pyotp
from requests_oauthlib import OAuth2Session
from transitions import Machine

from aitm.msft_aama.state_machine.actions import (
    add_security_info,
    authorize_mobileapp,
    initialize_mobileapp_registration,
    prepare_session,
    verify_security_info,
)


class StateMachine(Machine):
    """
    Represents a state machine for the registration process.

    This state machine manages the flow of the registration process, including capturing a session,
    preparing the session, authorizing the registration, initializing the registration, adding security info,
    verifying the added info, and emitting events.

    Attributes:
        _session (OAuth2Session | None): The captured session.
        _secret_key (str | None): The secret key for the registration.
        _session_ctx (str | None): The session context.

    Methods:
        on_session_captured: Event handler for when a session is captured.
        on_session_prepared: Event handler for when a session is prepared.
        on_registration_authorized: Event handler for when the registration is authorized.
        on_registration_initialized: Event handler for when the registration is initialized.
        on_info_added: Event handler for when security info is added.
        on_info_verified: Event handler for when the added info is verified.
        on_exception_raised: Event handler for when an exception is raised.
        on_event_emitted: Event handler for when an event is emitted.
    """

    class States(Enum):
        IDLE = 0
        PREPARING_SESSION = 1
        AUTHORIZING_REGISTRATION = 2
        INITIALIZING_REGISTRATION = 3
        ADDING_INFO = 4
        VERIFYING_INFO = 5
        COMPLETED = 6
        ERROR = 7

    _transitions = [
        {
            "trigger": "session_captured",
            "source": States.IDLE,
            "dest": States.PREPARING_SESSION,
            "after": "on_session_captured",
        },
        {
            "trigger": "session_prepared",
            "source": States.PREPARING_SESSION,
            "dest": States.AUTHORIZING_REGISTRATION,
            "after": "on_session_prepared",
        },
        {
            "trigger": "registration_authorized",
            "source": States.AUTHORIZING_REGISTRATION,
            "dest": States.INITIALIZING_REGISTRATION,
            "after": "on_registration_authorized",
        },
        {
            "trigger": "registration_initialized",
            "source": States.INITIALIZING_REGISTRATION,
            "dest": States.ADDING_INFO,
            "after": "on_registration_initialized",
        },
        {
            "trigger": "info_added",
            "source": States.ADDING_INFO,
            "dest": States.VERIFYING_INFO,
            "after": "on_info_added",
        },
        {
            "trigger": "info_verified",
            "source": States.VERIFYING_INFO,
            "dest": States.COMPLETED,
            "after": "on_info_verified",
        },
        {
            "trigger": "event_emitted",
            "source": [States.COMPLETED, States.ERROR],
            "dest": States.IDLE,
            "before": "on_event_emitted",
        },
        {"trigger": "exception_raised", "source": "*", "dest": States.ERROR, "after": "on_exception_raised"},
    ]
    _session: OAuth2Session | None = None
    _secret_key: str | None = None
    _session_ctx: str | None = None

    def __init__(self, **kwargs):
        super().__init__(
            states=self.States,
            transitions=self._transitions,
            initial="IDLE",
            auto_transitions=False,
            queued=True,
            **kwargs,
        )

    def on_session_captured(self, cookies: list[dict[str, str]], user_agent: str):
        """
        Event handler for when a session is captured.

        Args:
            cookies (list[dict[str, str]]): The captured session cookies.
            user_agent (str): The user agent string.
        """
        print("Session captured")
        try:
            self._session = prepare_session(cookies, user_agent)
            self.session_prepared()
        except Exception as e:
            self.exception_raised(e)

    def on_session_prepared(self):
        """
        Event handler for when a session is prepared.
        """
        print("Session prepared")
        try:
            self._session_ctx = authorize_mobileapp(self._session)
            self.registration_authorized()
        except Exception as e:
            self.exception_raised(e)

    def on_registration_authorized(self):
        """
        Event handler for when the registration is authorized.
        """
        print("Registration authorized")
        try:
            self._secret_key = initialize_mobileapp_registration(self._session, self._session_ctx)["SecretKey"]
            self.registration_initialized()
        except Exception as e:
            self.exception_raised(e)

    def on_registration_initialized(self):
        """
        Event handler for when the registration is initialized.
        """
        print("Registration initialized")
        try:
            verification_context = add_security_info(self._session, self._secret_key, self._session_ctx)[
                "VerificationContext"
            ]
            self.info_added(verification_context, pyotp.TOTP(self._secret_key).now())
        except Exception as e:
            self.exception_raised(e)

    def on_info_added(self, verification_context: str, otp_code: str):
        """
        Event handler for when security info is added.

        Args:
            verification_context (str): The verification context.
            otp_code (str): The OTP code.
        """
        print("Info added")
        try:
            verify_security_info(self._session, verification_context, otp_code, self._session_ctx)
            self.info_verified()
        except Exception as e:
            self.exception_raised(e)

    def on_info_verified(self):
        """
        Event handler for when the added info is verified.
        """
        print("Info verified")
        # TODO Emit event
        self.event_emitted()

    def on_exception_raised(self, exception):
        """
        Event handler for when an exception is raised.

        Args:
            exception: The raised exception.
        """
        print(f"Exception raised: {exception}")
        # TODO Emit event
        self.event_emitted()

    def on_event_emitted(self):
        """
        Event handler for when an event is emitted.
        """
        print("Event emitted")
        self._session = None
        self._secret_key = None
        self._session_ctx = None
