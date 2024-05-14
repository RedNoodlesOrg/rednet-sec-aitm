"""
Helper functions for request manipulations
"""

from __future__ import annotations

from http.cookies import SimpleCookie

from mitmproxy.http import HTTPFlow

from aitm.aitm_config import config


def modify_header(flow: HTTPFlow, header: str) -> None:
    """
    Function to modify the headers of a response
    """
    if flow.response is None:
        return None
    value = flow.response.headers.get(header)
    if value is not None:
        for target in config.targets:
            value = value.replace(target["origin"], target["proxy"])
        flow.response.headers[header] = value
    return None


def modify_content(flow: HTTPFlow) -> None:
    """
    Function to modify body of a response
    """
    if (
        flow.response is None
        or flow.server_conn is None
        or flow.response.text is None
        or flow.server_conn.address is None
    ):
        return None
    mime = flow.response.headers.get("Content-Type", "").split(";")[0]
    site = flow.server_conn.address[0]
    if mime in config.content_types and site in config.target_sites:
        for target in config.targets:
            flow.response.text = flow.response.text.replace(
                f'https://{target["origin"]}', f'https://{target["proxy"]}'
            )

    for mod in config.custom_modifications:
        if mime in mod["mimes"] and site in mod["sites"]:
            flow.response.text = flow.response.text.replace(
                mod["search"], mod["replace"]
            )
    return None


def modify_cookies(flow: HTTPFlow) -> None:
    """
    Function to modify set-cookies of a response
    """
    if flow.response is None:
        return None
    set_cookies_str = flow.response.headers.get_all("set-cookie")
    set_cookies_str_modified: list[str] = []

    if set_cookies_str:
        for cookie in set_cookies_str:
            for target in config.targets:
                cookie = cookie.replace(target["origin"], target["proxy"])
            set_cookies_str_modified.append(cookie)
        flow.response.headers.set_all("set-cookie", set_cookies_str_modified)
    return None


def save_cookies(flow: HTTPFlow, simple_cookie: SimpleCookie) -> None:
    """
    Function to load cookies into SimpleCookie
    """
    if flow.response is None:
        return None
    set_cookies_str = flow.response.headers.get_all("set-cookie")
    if set_cookies_str:
        for cookie in set_cookies_str:
            simple_cookie.load(cookie)
    return None
