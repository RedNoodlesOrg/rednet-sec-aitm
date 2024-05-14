"""
Main script that start mitmproxy
"""

from __future__ import annotations

import asyncio
import logging

from mitmproxy import options
from mitmproxy.tools import dump

from aitm.aitm_config import config
from aitm.modifier_addon import ModifierAddon
from aitm.upstream_addon import UpstreamAddon

logging.root.setLevel("INFO")


async def start_proxy(proxies: list[str]):
    """
    Async Method to run the proxy
    """
    opts = options.Options(
        showhost=True,
        listen_host="0.0.0.0",
        listen_port=443,
        mode=proxies,
        certs=["certs/fullchain.pem"],
        ssl_insecure=True,
    )

    master = dump.DumpMaster(
        opts,
        with_termlog=True,
        with_dumper=False,
    )

    master.addons.add(UpstreamAddon())
    master.addons.add(ModifierAddon())
    master.options.set("block_global=false")
    master.options.set("connection_strategy=lazy")
    await master.run()
    return master


if __name__ == "__main__":
    reverse_proxies = [
        f"reverse:https://{target['origin']}@{target['port']}"
        for target in config.targets
    ]
    reverse_proxies.append("upstream:https://dummy:8888")
    asyncio.run(start_proxy(reverse_proxies))
