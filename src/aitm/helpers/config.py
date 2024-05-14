"""
Config script
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypeAlias, TypedDict


class Target(TypedDict):
    """
    Target class
    """

    origin: str
    proxy: str
    port: int


class Modification(TypedDict):
    """
    Modification Class
    """

    mimes: list[str]
    sites: list[str]
    search: str
    replace: str


SchemeType: TypeAlias = Literal[
    "http", "https", "http3", "tls", "dtls", "tcp", "udp", "dns", "quic"
]


@dataclass
class Config:
    """
    Config Dataclass
    """

    _targets: list[Target] = field(default_factory=list)
    content_types: list[str] = field(default_factory=list)
    custom_modifications: list[Modification] = field(default_factory=list)
    auth_url: list[str] = field(default_factory=list)
    local_upstream_scheme: SchemeType = "http"
    local_upstream_hostname: str = ""
    _target_sites: list[str] = field(default_factory=list)
    _target_proxies: list[str] = field(default_factory=list)
    mfa_claim: str = ""

    @property
    def targets(self):
        """
        Getter of targets
        """
        return self._targets

    @targets.setter
    def targets(self, value: list[Target]):
        """
        Setter of targets
        """
        self._targets = value
        self._target_sites = [target["origin"] for target in value]
        self._target_proxies = [target["proxy"] for target in value]

    @targets.deleter
    def targets(self):
        """
        Deleting
        """
        del self._targets
        del self._target_proxies
        del self._target_sites

    @property
    def target_sites(self):
        """Getter of target_sites"""
        return self._target_sites

    @property
    def target_proxies(self):
        """Getter of target_proxies"""
        return self._target_proxies
