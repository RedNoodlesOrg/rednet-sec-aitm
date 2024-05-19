from __future__ import annotations

import requests
from jsonschema import validate


class PostRequest:
    """
    Represents a POST request.

    Attributes:
        BASE_URL (str): The base URL for the request.
        url (str): The URL for the request.
        headers (dict | None): The headers for the request.
        data (dict | None): The data for the request.
        cookies (dict | None): The cookies for the request.
        responseDataSchema (dict | None): The schema for the response data.
    """

    BASE_URL = "https://account.activedirectory.windowsazure.com/securityinfo/"

    url: str
    headers: dict | None = None
    data: dict | None = None
    cookies: dict | None = None
    responseDataSchema: dict

    def post_verify(self) -> dict | None:
        """
        Sends a POST request to the specified URL with the provided headers, data, and cookies.
        Validates the response against the specified JSON schema.

        Returns:
            dict or None: The JSON response from the server, or None if the request failed.
        """
        response = requests.post(url=self.url, headers=self.headers, data=self.data, cookies=self.cookies, timeout=10)
        response.raise_for_status()
        validate(instance=response.json(), schema=self.responseDataSchema)
        return response.json()
