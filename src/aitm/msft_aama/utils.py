from __future__ import annotations

import base64
import json
import logging
from urllib.parse import parse_qs, urlparse

from jsonschema import validate
from requests import Session
from requests_oauthlib import OAuth2Session

from ..aitm_config import config
from .config import AUTH_SCOPES, AUTH_URL, CLIENT_ID, REDIRECT_URI
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


def create_oauth2_session(session: Session) -> OAuth2Session:
    """
    Create and configure an OAuth2 session.

    Args:
        session (Session): The existing session object.

    Returns:
        OAuth2Session: The configured OAuth2 session.

    """
    auth_session = OAuth2Session(
        client_id=CLIENT_ID,
        scope=AUTH_SCOPES,
        redirect_uri=REDIRECT_URI,
        pkce="S256",
    )
    auth_session.cookies = session.cookies
    auth_session.headers = session.headers
    return auth_session


def get_authorization_url(auth_session: OAuth2Session) -> tuple[str, dict[str, list[str]]]:
    """
    Generate the authorization URL with additional parameters.

    Parameters:
        auth_session (OAuth2Session): The OAuth2 session object.

    Returns:
        Tuple[str, dict]: A tuple containing the base URL and the parameters dictionary.

    """
    authorization_url, _ = auth_session.authorization_url(AUTH_URL, access_type="offline")
    parsed_url = urlparse(authorization_url)
    params = parse_qs(parsed_url.query)
    params["claims"] = config.mfa_claim
    base_url = parsed_url._replace(query=None).geturl()
    return base_url, params
