from __future__ import annotations

from .PostRequest import PostRequest


class AddSecurityInfo(PostRequest):
    """
    Represents a class for adding security information.

    Attributes:
        url (str): The URL for the AddSecurityInfo endpoint.
        responseDataSchema (dict): The JSON schema for the response data.
        data (dict): The data to be sent in the request.

    Methods:
        __init__(secret_key: str): Initializes a new instance of the AddSecurityInfo class.
    """

    url = PostRequest.BASE_URL + "AddSecurityInfo"
    responseDataSchema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "Type": {"type": "number"},
            "VerificationState": {"type": "number"},
            "Data": {},
            "VerificationContext": {"type": "string"},
            "ErrorCode": {"type": "number"},
        },
        "required": ["Type", "VerificationState", "Data", "VerificationContext", "ErrorCode"],
    }

    data: dict

    def __init__(self, secret_key: str, cookies: dict | None = None) -> None:
        """
        Initializes a new instance of the AddSecurityInfo class.

        Args:
            secret_key (str): The secret key to be added as security information.
        """
        super().__init__()
        self.data = {
            "Type": 3,
            "Data": {"secretKey": f"{secret_key}", "affinityRegion": "null", "isResendNotificationChallenge": "false"},
        }
        self.cookies = cookies

    def _additional_verify(self, response: dict) -> None:
        """
        Verifies the additional response data for the AddSecurityInfo endpoint.

        Args:
            response (dict): The response data to verify.
        """
        assert response["Type"] == 3
        assert response["VerificationState"] == 1
        assert response["ErrorCode"] == 0
