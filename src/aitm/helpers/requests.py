"""
Helper functions for request manipulations
"""

from __future__ import annotations

from mitmproxy.http import HTTPFlow

from aitm.aitm_config import config


def modify_header(flow: HTTPFlow, header: str) -> None:
    """
    Function to modify the headers of a request
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
    Function to modify the query of a request
    """
    value = flow.request.query.get(query_key)
    if value is not None:
        for target in config.targets:
            value = value.replace(target["proxy"], target["origin"])
        flow.request.query[query_key] = value


def get_local_upstream_port(host: str) -> int | None:
    """
    Function to get the local upstream port
    """
    split = host.split(":")
    if len(split) == 2:
        if split[0] == "local.fsoc.bid":
            return int(split[1])
    return None


def modify_host(flow: HTTPFlow) -> None:
    """
    Function to modify the host
    """
    host = flow.request.headers.get("Host")
    if host is not None:
        port = get_local_upstream_port(host)
        origin = None
        if port is not None:
            origin = next(
                (
                    target["origin"]
                    for target in config.targets
                    if target["port"] == port
                ),
                None,
            )
        elif host in config.target_proxies:
            origin = next(
                (
                    target["origin"]
                    for target in config.targets
                    if target["proxy"] == host
                ),
                None,
            )
        if origin is not None:
            flow.request.headers["Host"] = origin
