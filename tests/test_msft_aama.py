from __future__ import annotations

import json
from http.cookies import SimpleCookie
from unittest.mock import patch

import requests
import requests_mock
from hypothesis import given
from hypothesis_jsonschema import from_schema

from aitm.msft_aama.config import (ADD_SECURITY_INFO_URL,
                                   INITIALIZE_MOBILE_APP_URL,
                                   VERIFY_SECURITY_INFO_URL)
from aitm.msft_aama.main import (add_security_info,
                                 initialize_mobileapp_registration, run,
                                 verify_security_info)
from aitm.msft_aama.schemas import (ADD_SECURITY_INFO_SCHEMA,
                                    INITIALIZE_MOBILE_APP_SCHEMA,
                                    VERIFY_SECURITY_INFO_SCHEMA)


@given(from_schema(VERIFY_SECURITY_INFO_SCHEMA))
def test_verify_security_info(mock_response):
    session = requests.Session()
    cookies = SimpleCookie()
    user_agent = "Test User Agent"
    cookies["cookie_name"] = "cookie_value"
    session.cookies.update(cookies)
    session.headers.update({"User-Agent": user_agent})

    verification_context = "test_verification_context"
    otp_code = "123456"
    mock_response = {"Type": 3, "VerificationState": 2, "ErrorCode": 0}
    mock_response_text = ")]}',\n" + json.dumps({"Type": 3, "VerificationState": 2, "ErrorCode": 0})
    with requests_mock.mock() as m:
        options_adapter = m.options(VERIFY_SECURITY_INFO_URL, status_code=200)
        post_adapter = m.post(VERIFY_SECURITY_INFO_URL, text=mock_response_text)

        response = verify_security_info(session, verification_context, otp_code)

        assert response == mock_response

        assert options_adapter.called
        assert post_adapter.called

        assert post_adapter.last_request.json() == {
            "Type": 3,
            "Data": json.dumps(
                {
                    "Type": 3,
                    "VerificationContext": verification_context,
                    "VerificationData": otp_code,
                }
            ),
        }


@given(from_schema(ADD_SECURITY_INFO_SCHEMA))
def test_add_security_info(mock_response):
    session = requests.Session()
    cookies = SimpleCookie()
    user_agent = "Test User Agent"
    cookies["cookie_name"] = "cookie_value"
    session.cookies.update(cookies)
    session.headers.update({"User-Agent": user_agent})

    secret_key = "test_secret_key"

    with requests_mock.Mocker() as m:
        mock_response.update({"Type": 3, "VerificationState": 1, "ErrorCode": 0})
        options_adapter = m.options(ADD_SECURITY_INFO_URL, status_code=200)
        post_adapter = m.post(ADD_SECURITY_INFO_URL, json=mock_response)

        response = add_security_info(session, secret_key)

        assert response == mock_response

        assert options_adapter.called
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
    session = requests.Session()
    cookies = SimpleCookie()
    user_agent = "Test User Agent"
    cookies["cookie_name"] = "cookie_value"
    session.cookies.update(cookies)
    session.headers.update({"User-Agent": user_agent})

    with requests_mock.Mocker() as m:
        mock_response.update({"RegistrationType": 3})
        options_adapter = m.options(INITIALIZE_MOBILE_APP_URL, status_code=200)
        post_adapter = m.post(INITIALIZE_MOBILE_APP_URL, json=mock_response)

        response = initialize_mobileapp_registration(session)

        assert response == mock_response
        assert response["RegistrationType"] == 3
        assert options_adapter.called
        assert post_adapter.called

        assert post_adapter.last_request.json() == {"securityInfoType": 3}


def test_run():
    cookies = SimpleCookie()
    user_agent = "Test User Agent"
    cookies["cookie_name"] = "cookie_value"

    with (
        patch("aitm.msft_aama.main.initialize_mobileapp_registration") as mock_initialize_mobileapp_registration,
        patch("aitm.msft_aama.main.add_security_info") as mock_add_security_info,
        patch("aitm.msft_aama.main.verify_security_info") as mock_verify_security_info,
    ):

        mock_initialize_mobileapp_registration.return_value = {"SecretKey": "5jm2hkk5jfn7s6dj"}
        mock_add_security_info.return_value = {"VerificationContext": "test_verification_context"}

        run(cookies, user_agent)

        assert mock_initialize_mobileapp_registration.called
        assert mock_add_security_info.called
        assert mock_verify_security_info.called
