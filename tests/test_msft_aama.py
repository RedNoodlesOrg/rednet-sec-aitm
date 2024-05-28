from __future__ import annotations

import base64
import json
from unittest.mock import MagicMock, patch

import requests_mock
from hypothesis import given
from hypothesis_jsonschema import from_schema
from requests import Session
from requests_oauthlib import OAuth2Session

from aitm.msft_aama.config import (
    ADD_SECURITY_INFO_URL,
    AUTHORIZE_MOBILE_APP_URL,
    INITIALIZE_MOBILE_APP_URL,
    VERIFY_SECURITY_INFO_URL,
)
from aitm.msft_aama.main import (
    add_security_info,
    authorize,
    authorize_mobileapp,
    initialize_mobileapp_registration,
    run,
    verify_security_info,
)
from aitm.msft_aama.schemas import (
    ADD_SECURITY_INFO_SCHEMA,
    AUTHORIZE_MOBILE_APP_SCHEMA,
    INITIALIZE_MOBILE_APP_SCHEMA,
)
from aitm.msft_aama.utils import get_tenant_id


def test_authorize():
    session = Session()
    with (
        patch("aitm.msft_aama.main.create_oauth2_session") as mock_create_oauth2_session,
        patch("aitm.msft_aama.main.get_authorization_url") as mock_get_authorization_url,
        patch("aitm.msft_aama.main.get_tenant_id") as mock_get_tenant_id,
        patch("aitm.msft_aama.main.OAuth2Session.fetch_token") as mock_fetch_token,
        patch("aitm.msft_aama.main.OAuth2Session.refresh_token") as mock_refresh_token,
    ):
        mock_create_oauth2_session.return_value = OAuth2Session()
        mock_get_authorization_url.return_value = ("https://example.com/authorize", {})
        mock_get_tenant_id.return_value = "dummy_tenant_id"
        mock_fetch_token.return_value = {
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token",
        }
        mock_refresh_token.return_value = {
            "access_token": "dummy_access_token",
            "refresh_token": "dummy_refresh_token",
        }

        result = authorize(session)

        assert isinstance(result, OAuth2Session)
        mock_create_oauth2_session.assert_called_once_with(session)
        mock_get_authorization_url.assert_called_once_with(mock_create_oauth2_session.return_value)
        mock_get_tenant_id.assert_called_once_with(mock_create_oauth2_session.return_value)


def test_get_tenant_id():
    session = MagicMock()
    tid = "12345678-1234-1234-1234-123456789abc"
    access_token_s1 = {
        "aud": "https://webshell.suite.office.com",
        "acr": "1",
        "amr": ["pwd", "mfa"],
        "tid": tid,
        "xms_tdbr": "EU",
    }
    access_token_s1 = json.dumps(access_token_s1).encode("utf-8")
    access_token_s1 = base64.urlsafe_b64encode(access_token_s1).decode("utf-8")
    access_token_s1 = access_token_s1.rstrip("=")
    access_token = f"eyJhbGciOi.{access_token_s1}.SflKxw"
    session.token = {"access_token": access_token}
    tenant_id = get_tenant_id(session)
    assert tenant_id == tid


@given(from_schema(AUTHORIZE_MOBILE_APP_SCHEMA))
def test_authorize_mobileapp(mock_response):
    session, ctx = MagicMock(), "test_session_ctx"

    with requests_mock.mock() as m:
        mock_response.update(
            {
                "isAuthorized": True,
                "sessionCtx": ctx,
            }
        )
        post_adapter = m.post(AUTHORIZE_MOBILE_APP_URL, json=mock_response)

        response = authorize_mobileapp(session)

        assert response == "test_session_ctx"
        assert post_adapter.called


def test_verify_security_info():
    session, ctx = MagicMock(), "test_session_ctx"
    verification_context = "test_verification_context"
    otp_code = "123456"
    mock_response = {"Type": 3, "VerificationState": 2, "ErrorCode": 0}
    mock_response_text = ")]}',\n" + json.dumps({"Type": 3, "VerificationState": 2, "ErrorCode": 0})
    with requests_mock.mock() as m:
        post_adapter = m.post(VERIFY_SECURITY_INFO_URL, text=mock_response_text)

        response = verify_security_info(session, verification_context, otp_code, ctx)

        assert response == mock_response

        assert post_adapter.called

        assert post_adapter.last_request.json() == {
            "Type": 3,
            "VerificationContext": verification_context,
            "VerificationData": otp_code,
        }


@given(from_schema(ADD_SECURITY_INFO_SCHEMA))
def test_add_security_info(mock_response):
    session, ctx = MagicMock(), "test_session_ctx"
    secret_key = "test_secret_key"

    with requests_mock.Mocker() as m:
        mock_response.update({"Type": 3, "VerificationState": 1, "ErrorCode": 0})
        post_adapter = m.post(ADD_SECURITY_INFO_URL, json=mock_response)

        response = add_security_info(session, secret_key, ctx)

        assert response == mock_response

        assert post_adapter.called

        assert post_adapter.last_request.json() == {
            "Type": 3,
            "Data": json.dumps(
                {
                    "secretKey": secret_key,
                    "affinityRegion": None,
                    "isResendNotificationChallenge": False,
                }
            ),
        }


@given(from_schema(INITIALIZE_MOBILE_APP_SCHEMA))
def test_initialize_mobileapp_registration(mock_response):
    session, ctx = MagicMock(), "test_session_ctx"

    with requests_mock.Mocker() as m:
        mock_response.update({"RegistrationType": 3})
        post_adapter = m.post(INITIALIZE_MOBILE_APP_URL, json=mock_response)

        response = initialize_mobileapp_registration(session, ctx)

        assert response == mock_response
        assert response["RegistrationType"] == 3
        assert post_adapter.called

        assert post_adapter.last_request.json() == {"securityInfoType": 3}


def test_run():
    cookies: list[dict[str, str]] = [
        {
            "name": "cookie_name",
            "value": "cookie_value",
            "domain": "cookie_domain",
        }
    ]
    user_agent = "Test User Agent"
    test_secret_key = "5jm2hkk5jfn7s6dj"

    with (
        patch("aitm.msft_aama.main.authorize") as mock_authorize,
        patch("aitm.msft_aama.main.authorize_mobileapp") as mock_authorize_mobileapp,
        patch("aitm.msft_aama.main.initialize_mobileapp_registration") as mock_initialize_mobileapp_registration,
        patch("aitm.msft_aama.main.add_security_info") as mock_add_security_info,
        patch("aitm.msft_aama.main.verify_security_info") as mock_verify_security_info,
    ):

        mock_authorize.return_value = "test_session"
        mock_authorize_mobileapp.return_value = {"sessionCtx": "test_session_ctx"}
        mock_initialize_mobileapp_registration.return_value = {"SecretKey": test_secret_key}
        mock_add_security_info.return_value = {"VerificationContext": "test_verification_context"}

        result_secret_key = run(cookies, user_agent)

        assert result_secret_key == test_secret_key
        assert mock_authorize_mobileapp.called
        assert mock_initialize_mobileapp_registration.called
        assert mock_add_security_info.called
        assert mock_verify_security_info.called
