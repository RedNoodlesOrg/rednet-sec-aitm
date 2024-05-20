from __future__ import annotations

import json
from http.cookies import SimpleCookie

import pyotp
from requests import Session

from .config import (ADD_SECURITY_INFO_URL, HEADERS, INITIALIZE_MOBILE_APP_URL,
                     VERIFY_SECURITY_INFO_URL)
from .schemas import (ADD_SECURITY_INFO_SCHEMA, INITIALIZE_MOBILE_APP_SCHEMA,
                      VERIFY_SECURITY_INFO_SCHEMA)
from .utils import send_request


def initialize_mobileapp_registration(session: Session) -> dict:
    """
    Initializes the mobile app registration.

    Args:
        session (Session): The session object for making requests.

    Returns:
        dict: The response from the mobile app registration API.

    Raises:
        AssertionError: If the registration type in the response is not 3.
    """
    data = {"securityInfoType": 3}
    response = send_request(session, INITIALIZE_MOBILE_APP_URL, data, INITIALIZE_MOBILE_APP_SCHEMA)
    assert response["RegistrationType"] == 3
    return response


def add_security_info(session: Session, secret_key: str) -> dict:
    """
    Adds security information to the session.

    Args:
        session (Session): The session object.
        secret_key (str): The secret key to be added.

    Returns:
        dict: The response from the server.

    Raises:
        AssertionError: If the response type, verification state, or error code is not as expected.
    """
    data = {
        "Type": 3,
        "Data": json.dumps({"secretKey": secret_key, "affinityRegion": None, "isResendNotificationChallenge": False}),
    }
    response = send_request(session, ADD_SECURITY_INFO_URL, data, ADD_SECURITY_INFO_SCHEMA)
    assert response["Type"] == 3
    assert response["VerificationState"] == 1
    assert response["ErrorCode"] == 0
    return response


def verify_security_info(session: Session, verification_context: str, otp_code: str) -> dict:
    """
    Verifies the security information using the provided session, verification context, and OTP code.

    Args:
        session (Session): The session object used for making the request.
        verification_context (str): The verification context.
        otp_code (str): The OTP code.

    Returns:
        dict: The response from the verification request.

    Raises:
        AssertionError: If the response type is not 3, the verification state is not 2, or the error code is not 0.
    """
    data = {
        "Type": 3,
        "Data": json.dumps(
            {
                "Type": 3,
                "VerificationContext": verification_context,
                "VerificationData": otp_code,
            }
        ),
    }
    response = send_request(session, VERIFY_SECURITY_INFO_URL, data, VERIFY_SECURITY_INFO_SCHEMA)
    assert response["Type"] == 3
    assert response["VerificationState"] == 2
    assert response["ErrorCode"] == 0
    return response


def run(cookies: SimpleCookie, user_agent: str):
    """
    Runs the main process for the AAMA (Add Authentication Method Automation) workflow.

    Args:
        cookies (SimpleCookie): The cookies to be used for the session.
        user_agent (str): The user agent string to be used for the session.

    Returns:
        None
    """
    session = Session()
    session.cookies.update(cookies)
    session.headers.update({"name": "User-Agent", "value": user_agent})
    session.headers.update(HEADERS)
    # Step 1: Initialize the mobile app registration
    secret_key = initialize_mobileapp_registration(session)["SecretKey"]
    totp = pyotp.TOTP(secret_key)
    # Step 2: Add security info
    verification_context = add_security_info(session, secret_key)["VerificationContext"]
    # Step 3: Verify the security info
    verify_security_info(session, verification_context, totp.now())
