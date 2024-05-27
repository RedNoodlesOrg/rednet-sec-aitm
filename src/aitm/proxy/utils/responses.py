"""
Helper functions for response manipulations in mitmproxy.
"""

from __future__ import annotations

from http.cookies import SimpleCookie

from mitmproxy.http import HTTPFlow

from .config import get_config


# TODO: Remove dependency on config.targets
def modify_header(flow: HTTPFlow, header: str) -> None:
    """
    Modifies the specified header in an HTTP response.

    This function updates the specified header in the response by replacing the
    original host with the proxy host as per the configuration targets.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
        header (str): The header name to modify.
    """
    if flow.response is None:
        return
    value = flow.response.headers.get(header)
    if value is not None:
        for target in get_config().targets:
            value = value.replace(target["origin"], target["proxy"])
        flow.response.headers[header] = value


def modify_content(flow: HTTPFlow) -> None:
    """
    Modifies the body of an HTTP response.

    This function updates the response body by replacing occurrences of the
    original host with the proxy host as per the configuration targets. It also
    applies custom modifications based on MIME type and site URL.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
    """
    if (
        flow.response is None
        or flow.server_conn is None
        or flow.response.text is None
        or flow.server_conn.address is None
    ):
        return
    mime = flow.response.headers.get("Content-Type", "").split(";")[0]
    site = flow.server_conn.address[0]
    if mime in get_config().content_types and site in get_config().target_sites:
        for target in get_config().targets:
            flow.response.text = flow.response.text.replace(f'https://{target["origin"]}', f'https://{target["proxy"]}')

    for mod in get_config().custom_modifications:
        if mime in mod["mimes"] and site in mod["sites"]:
            flow.response.text = flow.response.text.replace(mod["search"], mod["replace"])


def modify_cookies(flow: HTTPFlow) -> None:
    """
    Modifies the Set-Cookie headers in an HTTP response.

    This function updates the Set-Cookie headers in the response by replacing
    occurrences of the original host with the proxy host as per the configuration
    targets.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
    """
    if flow.response is None:
        return
    set_cookies_str = flow.response.headers.get_all("set-cookie")
    set_cookies_str_modified: list[str] = []

    if set_cookies_str:
        for cookie in set_cookies_str:
            for target in get_config().targets:
                cookie = cookie.replace(target["origin"], target["proxy"])
            set_cookies_str_modified.append(cookie)
        flow.response.headers.set_all("set-cookie", set_cookies_str_modified)


def save_cookies(flow: HTTPFlow, simple_cookie: SimpleCookie) -> None:
    """
    Loads cookies from the HTTP response into a SimpleCookie object.

    This function extracts Set-Cookie headers from the response and loads them
    into the provided SimpleCookie object.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
        simple_cookie (SimpleCookie): The SimpleCookie object to load cookies into.
    """
    if flow.response is None:
        return
    set_cookies_str = flow.response.headers.get_all("set-cookie")
    if set_cookies_str:
        for cookie in set_cookies_str:
            simple_cookie.load(cookie)
