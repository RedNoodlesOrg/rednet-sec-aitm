from __future__ import annotations

import base64
import json
import logging

from jsonschema import validate
from requests_oauthlib import OAuth2Session

from .requests import PostRequest

logger = logging.getLogger(__name__)


def send_request(
    session: OAuth2Session, url: str, schema: dict, data: dict | None = None, sessionCtx: str | None = None
) -> dict:
    """
    Sends a request to the specified URL using the provided session, data, and schema.

    Args:
        session (Session): The session object to use for sending the request.
        url (str): The URL to send the request to.
        data (dict): The data to include in the request.
        schema (dict): The schema to validate the response against.

    Returns:
        dict: The response JSON as a dictionary.

    Raises:
        HTTPError: If the request or response encounters an error.
        JSONDecodeError: If the response JSON cannot be decoded.
        ValidationError: If the response JSON does not match the provided schema.
    """

    post = PostRequest().send(session=session, url=url, data=data, sessionCtx=sessionCtx)
    post.raise_for_status()
    response_json = parse_garbage(post.text)
    validate(instance=response_json, schema=schema)
    return response_json


def parse_garbage(data: str) -> dict:
    """
    Parses garbage text from the beginning of a JSON response.

    Args:
        data (str): The response text to parse.

    Returns:
        dict: The cleaned and parsed data.
    """
    if data.startswith(")]}',\n"):
        return json.loads(data[5:])
    return json.loads(data)


def get_tenant_id(session: OAuth2Session) -> str:
    """
    Gets the tenant ID from the session.

    Args:
        session (Session): The session object to use for sending the request.

    Returns:
        str: The tenant ID.
    """
    sections = session.token["access_token"].split(".")
    payload = sections[1]

    payload_bytes = base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
    payload_string = payload_bytes.decode("utf-8")
    payload_json = json.loads(payload_string)
    return payload_json["tid"]
