"""
Upstream addon for mitmproxy.
"""

from __future__ import annotations

import logging

from mitmproxy.http import HTTPFlow

from aitm.aitm_config import config

logger = logging.getLogger(__name__)


def proxy_port(flow: HTTPFlow) -> int | None:
    """
    Gets the correct port for the upstream proxy based on the request host.

    This function checks the configuration targets and returns the corresponding
    port number for the upstream proxy if the request host matches a target.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing
                                        the client request and server response.

    Returns:
        int | None: The port number for the upstream proxy, or None if no match is found.
    """
    for target in config.targets:
        if target["proxy"] == flow.request.host:
            return target["port"]
    return None


class UpstreamAddon:
    """
    Addon Class for the upstream proxy.

    This addon redirects requests to a specified upstream proxy based on the configuration.
    """

    def request(self, flow: HTTPFlow) -> None:
        """
        Modifies the HTTP request to use an upstream proxy.

        This method is called by mitmproxy for each HTTP request. It updates the
        request to route through a specified upstream proxy if the request host
        matches any of the configured target proxies.

        Args:
            flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing
                                            the client request and server response.
        """
        if flow.request.host in config.target_proxies:
            port = proxy_port(flow)
            if port is not None:
                flow.server_conn.via = config.local_upstream_scheme, (
                    config.local_upstream_hostname,
                    port,
                )
                flow.request.host = config.local_upstream_hostname
                flow.request.port = port
                flow.request.scheme = config.local_upstream_scheme
