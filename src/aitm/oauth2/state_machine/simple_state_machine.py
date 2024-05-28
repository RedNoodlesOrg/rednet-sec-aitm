from __future__ import annotations

import logging
from enum import Enum

import pyotp
from requests_oauthlib import OAuth2Session

from .actions import (
    add_security_info,
    authorize_mobileapp,
    initialize_mobileapp_registration,
    prepare_session,
    verify_security_info,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleStateMachine:
    """
    Represents a simplified state machine for the registration process.

    This state machine manages the flow of the registration process, including capturing a session,
    preparing the session, authorizing the registration, initializing the registration, adding security info,
    verifying the added info, and emitting events.

    Attributes:
        _session (OAuth2Session | None): The captured session.
        _secret_key (str | None): The secret key for the registration.
        _session_ctx (str | None): The session context.

    Methods:
        start: Begins the registration process.
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

    def __init__(self):
        self.state = self.States.IDLE
        self._session: OAuth2Session | None = None
        self._secret_key: str | None = None
        self._session_ctx: str | None = None

    def start(self, cookies: list[dict[str, str]], user_agent: str):
        self.state = self.States.PREPARING_SESSION
        self.on_session_captured(cookies, user_agent)

    def on_session_captured(self, cookies: list[dict[str, str]], user_agent: str):
        logger.info("Session captured")
        try:
            self._session = prepare_session(cookies, user_agent)
            self.state = self.States.AUTHORIZING_REGISTRATION
            self.on_session_prepared()
        except Exception as e:
            self.on_exception_raised(e)

    def on_session_prepared(self):
        logger.info("Session prepared")
        try:
            self._session_ctx = authorize_mobileapp(self._session)
            self.state = self.States.INITIALIZING_REGISTRATION
            self.on_registration_authorized()
        except Exception as e:
            self.on_exception_raised(e)

    def on_registration_authorized(self):
        logger.info("Registration authorized")
        try:
            self._secret_key = initialize_mobileapp_registration(self._session, self._session_ctx)["SecretKey"]
            self.state = self.States.ADDING_INFO
            self.on_registration_initialized()
        except Exception as e:
            self.on_exception_raised(e)

    def on_registration_initialized(self):
        logger.info("Registration initialized")
        try:
            verification_context = add_security_info(self._session, self._secret_key, self._session_ctx)[
                "VerificationContext"
            ]
            self.state = self.States.VERIFYING_INFO
            self.on_info_added(verification_context, pyotp.TOTP(self._secret_key).now())
        except Exception as e:
            self.on_exception_raised(e)

    def on_info_added(self, verification_context: str, otp_code: str):
        logger.info("Info added")
        try:
            verify_security_info(self._session, verification_context, otp_code, self._session_ctx)
            self.state = self.States.COMPLETED
            self.on_info_verified()
        except Exception as e:
            self.on_exception_raised(e)

    def on_info_verified(self):
        logger.info("Info verified")
        self.on_event_emitted()

    def on_exception_raised(self, exception):
        logger.error(f"Exception raised: {exception}")
        self.state = self.States.ERROR
        self.on_event_emitted()

    def on_event_emitted(self):
        logger.info("Event emitted")
        self._session = None
        self._secret_key = None
        self._session_ctx = None
        self.state = self.States.IDLE
