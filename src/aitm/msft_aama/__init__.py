# flake8: noqa: F401
from __future__ import annotations

from .AddSecurityInfo import AddSecurityInfo
from .InitializeMobileAppRegistration import InitializeMobileAppRegistration
from .OTPGenerator import OTPGenerator
from .VerifySecurityInfo import VerifySecurityInfo


def register(cookies: dict) -> None:
    """
    Registers a new security method for the user.

    Args:
        cookies (dict): The cookies to be used in the request.

    Returns:
        None

    Raises:
        AssertionError: If the response from the server is None.

    """
    # Step 1: Initialize the mobile app registration
    imar = InitializeMobileAppRegistration(cookies=cookies)
    imar_response = imar.post_verify()

    # Step 2: Add security info
    asi = AddSecurityInfo(imar_response["SecretKey"], cookies=cookies)
    asi_response = asi.post_verify()

    # Step 3: Verify the security info
    vsi = VerifySecurityInfo(
        verification_context=asi_response["VerificationContext"],
        otp_code=OTPGenerator(imar_response["SecretKey"]).generate_otp(),
        cookies=cookies,
    )
    vsi_response = vsi.post_verify()

    assert vsi_response is not None
