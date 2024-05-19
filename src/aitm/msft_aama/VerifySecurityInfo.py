from __future__ import annotations

from requests import Session

from .PostRequest import PostRequest


class VerifySecurityInfo(PostRequest):
    """
    Represents a class for verifying security information.

    Attributes:
        url (str): The URL for the VerifySecurityInfo endpoint.
        responseDataSchema (dict): The JSON schema for the response data.
        data (dict): The data to be sent in the request.

    Args:
        verification_context (str): The verification context.
        otp_code (str): The OTP code for verification.
    """

    url = PostRequest.BASE_URL + "VerifySecurityInfo"
    responseDataSchema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "Type": {"type": "number"},
            "VerificationState": {"type": "number"},
            "DataUpdates": {
                "type": "object",
                "properties": {"DefaultMethodOptions": {"type": "number"}, "DefaultMethod": {"type": "number"}},
                "required": ["DefaultMethodOptions", "DefaultMethod"],
            },
            "ErrorCode": {"type": "number"},
        },
        "required": ["Type", "VerificationState", "DataUpdates", "ErrorCode"],
    }

    data: dict

    def __init__(self, verification_context: str, otp_code: str, session: Session) -> None:
        """
        Initializes a new instance of the VerifySecurityInfo class.

        Args:
            verification_context (str): The verification context.
            otp_code (str): The OTP code.

        Returns:
            None
        """
        super().__init__(session=session)
        self.data = {
            "Type": 3,
            "VerificationContext": f"{verification_context}",
            "VerificationData": f"{otp_code}",
        }

    def _additional_verify(self, response: dict) -> None:
        """
        Verifies the additional response data for the VerifySecurityInfo endpoint.

        Args:
            response (dict): The response data to verify.

        Returns:
            None
        """
        assert response["Type"] == 3
        assert response["VerificationState"] == 2
        assert response["ErrorCode"] == 0
