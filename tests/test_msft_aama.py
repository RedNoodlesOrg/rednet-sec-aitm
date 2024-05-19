from __future__ import annotations

import pyotp
import pytest
import requests_mock

from aitm.msft_aama import (AddSecurityInfo, InitializeMobileAppRegistration,
                            OTPGenerator, VerifySecurityInfo)


@pytest.mark.integration
def test_aama():
    """
    Test case for the AAMA (Add Authentication Method Automation) flow.

    This test case performs the following steps:
    1. Generates a random secret key using pyotp.
    2. Initializes the mobile app registration by making a POST request to the InitializeMobileAppRegistration endpoint.
    3. Adds security info by making a POST request to the AddSecurityInfo endpoint.
    4. Verifies the security info by making a POST request to the VerifySecurityInfo endpoint.
    5. Performs assertions to validate the responses from each step.

    Note: This test case requires the requests_mock library for mocking HTTP requests.

    Returns:
        None
    """
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key)

    imar_response = {
        "SecretKey": secret_key,
    }

    asi_respone = {
        "Type": 3,
        "VerificationState": 1,
        "Data": {},
        "VerificationContext": "SomeBase64String",
        "ErrorCode": 0,
    }

    vsi_response = {
        "Type": 3,
        "VerificationState": 2,
        "DataUpdates": {
            "DefaultMethodOptions": 3,
            "DefaultMethod": 0,
        },
        "ErrorCode": 0,
    }

    with requests_mock.Mocker(real_http=False) as m:
        m.post(VerifySecurityInfo.url, json=vsi_response)
        m.post(AddSecurityInfo.url, json=asi_respone)
        m.post(InitializeMobileAppRegistration.url, json=imar_response)

        step_1 = InitializeMobileAppRegistration()
        step_1_response = step_1.post_verify()

        assert step_1_response == imar_response

        otp_gen = OTPGenerator(step_1_response["SecretKey"])

        step_2 = AddSecurityInfo(step_1_response["SecretKey"])
        step_2_response = step_2.post_verify()

        assert step_2_response == asi_respone

        step_3 = VerifySecurityInfo(step_2_response["VerificationContext"], otp_gen.generate_otp())
        step_3_response = step_3.post_verify()

        assert step_3_response == vsi_response

        assert totp.now() == otp_gen.generate_otp()
        assert totp.verify(otp_gen.generate_otp())
