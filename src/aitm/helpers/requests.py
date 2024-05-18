"""
Helper functions for request manipulations in mitmproxy.
"""

from __future__ import annotations

from mitmproxy.http import HTTPFlow

from ..aitm_config import config


# TODO: Remove dependency on config.targets
def modify_header(flow: HTTPFlow, header: str) -> None:
    """
    Modifies the specified header in an HTTP request.

    This function updates the specified header in the request by replacing the
    proxy host with the original host as per the configuration targets. If the
    header is "Host", it calls a specific function to handle host modification.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
        header (str): The header name to modify.
    """
    if header == "Host":
        modify_host(flow)
    else:
        value = flow.request.headers.get(header)
        if value is not None:
            for target in config.targets:
                value = value.replace(target["proxy"], target["origin"])
            flow.request.headers[header] = value


def modify_query(flow: HTTPFlow, query_key: str) -> None:
    """
    Modifies the specified query parameter in an HTTP request.

    This function updates the specified query parameter by replacing the proxy
    host with the original host as per the configuration targets.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
        query_key (str): The query parameter name to modify.
    """
    value = flow.request.query.get(query_key)
    if value is not None:
        for target in config.targets:
            value = value.replace(target["proxy"], target["origin"])
        flow.request.query[query_key] = value


def get_local_upstream_port(host: str) -> int | None:
    """
    Gets the local upstream port based on the host.

    This function extracts the port number from the host string if the host is
    "local.fsoc.bid". Otherwise, it returns None.

    Args:
        host (str): The host string to extract the port from.

    Returns:
        int | None: The extracted port number, or None if not applicable.
    """
    split = host.split(":")
    if len(split) == 2:
        if split[0] == "local.fsoc.bid":
            return int(split[1])
    return None


def modify_host(flow: HTTPFlow) -> None:
    """
    Modifies the host header in an HTTP request.

    This function updates the "Host" header by replacing the proxy host with the
    original host as per the configuration targets. It also handles cases where
    the host includes a port number.

    Args:
        flow (mitmproxy.http.HTTPFlow): The HTTP flow object representing the client request.
    """
    host = flow.request.headers.get("Host")
    if host is not None:
        port = get_local_upstream_port(host)
        origin = None
        if port is not None:
            origin = next(
                (target["origin"] for target in config.targets if target["port"] == port),
                None,
            )
        elif host in config.target_proxies:
            origin = next(
                (target["origin"] for target in config.targets if target["proxy"] == host),
                None,
            )
        if origin is not None:
            flow.request.headers["Host"] = origin
