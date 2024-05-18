from __future__ import annotations


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
    headers: dict | None
    data: dict | None
    cookies: dict | None
    responseDataSchema: dict | None
