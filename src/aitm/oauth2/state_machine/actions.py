from __future__ import annotations

import json

from requests import Session
from requests_oauthlib import OAuth2Session

from aitm.oauth2.config import (
    ACCESS_SCOPES,
    ADD_SECURITY_INFO_URL,
    AUTHORIZE_MOBILE_APP_URL,
    HEADERS,
    INITIALIZE_MOBILE_APP_URL,
    TENANT_TOKEN_URL,
    TOKEN_URL,
    VERIFY_SECURITY_INFO_URL,
)
from aitm.oauth2.schemas import (
    ADD_SECURITY_INFO_SCHEMA,
    AUTHORIZE_MOBILE_APP_SCHEMA,
    INITIALIZE_MOBILE_APP_SCHEMA,
    VERIFY_SECURITY_INFO_SCHEMA,
)
from aitm.oauth2.utils import (
    create_oauth2_session,
    get_authorization_url,
    get_tenant_id,
    send_request,
)


def add_security_info(session: Session, secret_key: str, session_ctx: str) -> dict:
    """
    Adds security information to the session.

    Args:
        session (Session): The session object.
        secret_key (str): The secret key to be added.
        session_ctx (str): The session context.

    Returns:
        dict: The response from the server.

    Raises:
        AssertionError: If the response type, verification state, or error code is not as expected.
    """

    data = {
        "Type": 3,
        "Data": json.dumps({"secretKey": secret_key, "affinityRegion": None, "isResendNotificationChallenge": False}),
    }
    response = send_request(
        session=session, url=ADD_SECURITY_INFO_URL, data=data, schema=ADD_SECURITY_INFO_SCHEMA, sessionCtx=session_ctx
    )
    assert response["Type"] == 3
    assert response["VerificationState"] == 1
    assert response["ErrorCode"] == 0
    return response


def authorize_mobileapp(session: OAuth2Session) -> str:
    """
    Authorizes the mobile app using the provided session.

    Args:
        session (OAuth2Session): The session object used for authorization.

    Returns:
        str: The session context.

    Raises:
        AssertionError: If the authorization response is not valid.
    """

    response = send_request(session=session, url=AUTHORIZE_MOBILE_APP_URL, schema=AUTHORIZE_MOBILE_APP_SCHEMA)
    assert response["isAuthorized"]
    assert "sessionCtx" in response
    return response["sessionCtx"]


def initialize_mobileapp_registration(session: OAuth2Session, session_ctx: str) -> dict:
    """
    Initializes the mobile app registration.

    Args:
        session (OAuth2Session): The OAuth2 session.
        session_ctx (str): The session context.

    Returns:
        dict: The response from the server.

    Raises:
        AssertionError: If the registration type is not 3.
    """

    data = {"securityInfoType": 3}
    response = send_request(
        session=session,
        url=INITIALIZE_MOBILE_APP_URL,
        data=data,
        schema=INITIALIZE_MOBILE_APP_SCHEMA,
        sessionCtx=session_ctx,
    )
    assert response["RegistrationType"] == 3
    return response


def authorize(session: Session) -> OAuth2Session:
    """
    Authorizes the session using OAuth2 authentication.

    Args:
        session (Session): The session object.

    Returns:
        OAuth2Session: The authorized session object.
    """
    auth_session = create_oauth2_session(session)
    base_url, params = get_authorization_url(auth_session)
    auth_result = auth_session.get(base_url, params=params)
    token = auth_session.fetch_token(
        token_url=TOKEN_URL, authorization_response=auth_result.url, include_client_id=True
    )
    token = auth_session.refresh_token(token_url=TOKEN_URL, refresh_token=token["refresh_token"])
    tid = get_tenant_id(auth_session)
    tenant_token_url = TENANT_TOKEN_URL.format(tid=tid)
    for scope in ACCESS_SCOPES:
        auth_session.scope = scope
        token = auth_session.refresh_token(token_url=tenant_token_url, refresh_token=token["refresh_token"])

    return auth_session


def prepare_session(cookies: list[dict[str, str]], user_agent: str) -> OAuth2Session:
    """
    Prepares the session object with the provided cookies and user agent.

    Args:
        cookies (list[dict[str, str]]): The cookies to be used for the session.
        user_agent (str): The user agent string to be used for the session.

    Returns:
        Session: The session object with the provided cookies and user agent.
    """
    session = Session()
    for cookie in cookies:
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie["domain"],
        )
    session.headers.update({"User-Agent": user_agent})
    session.headers.update(HEADERS)
    return authorize(session)


def verify_security_info(session: Session, verification_context: str, otp_code: str, session_ctx: str) -> dict:
    """
    Verify the security information using the provided session, verification context, OTP code, and session context.

    Args:
        session (Session): The session object used for making the request.
        verification_context (str): The verification context.
        otp_code (str): The OTP code.
        session_ctx (str): The session context.

    Returns:
        dict: The response from the verification request.

    Raises:
        AssertionError: If the response type is not 3, the verification state is not 2, or the error code is not 0.
    """
    data = {
        "Type": 3,
        "VerificationContext": verification_context,
        "VerificationData": otp_code,
    }
    response = send_request(
        session=session,
        url=VERIFY_SECURITY_INFO_URL,
        data=data,
        schema=VERIFY_SECURITY_INFO_SCHEMA,
        sessionCtx=session_ctx,
    )
    assert response["Type"] == 3
    assert response["VerificationState"] == 2
    assert response["ErrorCode"] == 0
    return response
