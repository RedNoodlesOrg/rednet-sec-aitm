"""
Upstream addon
"""
from __future__ import annotations

import logging

from mitmproxy.http import HTTPFlow

from aitm.aitm_config import config

logger = logging.getLogger(__name__)


def proxy_port(flow: HTTPFlow) -> int | None:
    """
    Function to get the correct port for the upstream
    """
    for target in config.targets:
        if target["proxy"] == flow.request.host:
            return target["port"]
    return None


class UpstreamAddon:
    """
    Addon Class for the upstream proxy
    """

    def request(self, flow: HTTPFlow) -> None:
        """
        Method which mitmproxy calls for each request
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
