from __future__ import annotations

import json
import logging

from jsonschema import validate
from requests import Session

from .requests import OptionsRequest, PostRequest

logger = logging.getLogger(__name__)


def send_request(session: Session, url: str, data: dict, schema: dict) -> dict:
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
    options = OptionsRequest().send(session=session, url=url)
    options.raise_for_status()

    post = PostRequest().send(session=session, url=url, data=data)
    post.raise_for_status()

    response_text = post.text
    if response_text.startswith(")]}',\n"):
        response_text = response_text[5:]
    response_json = json.loads(response_text)

    validate(instance=response_json, schema=schema)
    return response_json
