"""
Helper functions for handling cookies.
"""

from __future__ import annotations

from http.cookies import SimpleCookie

from ..aitm_config import config


# TODO: Remove dependency on config.targets
def parse_cookies(cookies: SimpleCookie) -> list[dict[str, str]]:
    """
    Parses a SimpleCookie object into a list of dictionaries formatted for CookieEditor.

    This function converts a `SimpleCookie` object into a list of dictionaries,
    with each dictionary representing a cookie. The domain of each cookie is
    replaced with the corresponding origin from the configuration targets.

    Args:
        cookies (SimpleCookie): The SimpleCookie object to parse.

    Returns:
        list[dict[str, str]]: A list of dictionaries representing the parsed cookies.
    """
    parsed_cookies = []
    for name, morsel in cookies.items():
        cookie = {"name": name, "value": morsel.value}
        for k, v in morsel.items():
            if k == "domain":
                for target in config.targets:
                    v = v.replace(target["proxy"], target["origin"])
            cookie[k] = v
        parsed_cookies.append(cookie)
    return parsed_cookies
