from __future__ import annotations

from .PostRequest import PostRequest


class InitializeMobileAppRegistration(PostRequest):
    """
    Represents a class for initializing the mobile app registration.

    Attributes:
        url (str): The URL for the mobile app registration endpoint.
        data (dict): The data to be sent in the request.
        responseDataSchema (dict): The JSON schema for the expected response data.
    """

    url = PostRequest.BASE_URL + "InitializeMobileAppRegistration"
    data = {"securityInfoType": 3}
    responseDataSchema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"SecretKey": {"type": "string"}},
        "required": ["SecretKey"],
    }

    def __init__(self, cookies: dict | None = None) -> None:
        """
        Initializes a new instance of the InitializeMobileAppRegistration class.

        Args:
            cookies (dict): The cookies to be used in the request.
        """
        super().__init__()
        self.cookies = cookies
