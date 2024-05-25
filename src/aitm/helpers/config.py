"""
Configuration script for defining proxy and modification targets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypeAlias, TypedDict


class Target(TypedDict):
    """
    Represents a target configuration for the proxy.

    Attributes:
        origin (str): The origin URL of the target.
        proxy (str): The proxy address for the target.
        port (int): The port number to use for the proxy.
    """

    origin: str
    proxy: str
    port: int


class Modification(TypedDict):
    """
    Represents a modification rule for HTTP content.

    Attributes:
        mimes (list[str]): List of MIME types to apply the modification to.
        sites (list[str]): List of site URLs to apply the modification to.
        search (str): The string to search for in the content.
        replace (str): The string to replace the search string with.
    """

    mimes: list[str]
    sites: list[str]
    search: str
    replace: str


SchemeType: TypeAlias = Literal["http", "https", "http3", "tls", "dtls", "tcp", "udp", "dns", "quic"]


@dataclass
class Config:
    """
    Configuration dataclass for proxy and modification settings.

    Attributes:
        _targets (list[Target]): List of target configurations.
        content_types (list[str]): List of content types to filter.
        custom_modifications (list[Modification]): List of custom modification rules.
        auth_url (list[str]): List of URLs requiring authentication.
        local_upstream_scheme (SchemeType): Scheme type for the local upstream.
        local_upstream_hostname (str): Hostname for the local upstream.
        _target_sites (list[str]): List of target site URLs.
        _target_proxies (list[str]): List of target proxy addresses.
        mfa_claim (str): MFA claim string for authentication.
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
    def targets(self) -> list[Target]:
        """
        Gets the list of target configurations.

        Returns:
            list[Target]: The list of target configurations.
        """
        return self._targets

    @targets.setter
    def targets(self, value: list[Target]):
        """
        .. no-index::
        Sets the list of target configurations and updates associated attributes.

        Args:
            value (list[Target]): The new list of target configurations.
        """
        self._targets = value
        self._target_sites = [target["origin"] for target in value]
        self._target_proxies = [target["proxy"] for target in value]

    @targets.deleter
    def targets(self):
        """
        .. no-index::
        Deletes the target configurations and associated attributes.
        """
        del self._targets
        del self._target_proxies
        del self._target_sites

    @property
    def target_sites(self) -> list[str]:
        """
        Gets the list of target site URLs.

        Returns:
            list[str]: The list of target site URLs.
        """
        return self._target_sites

    @property
    def target_proxies(self) -> list[str]:
        """
        Gets the list of target proxy addresses.

        Returns:
            list[str]: The list of target proxy addresses.
        """
        return self._target_proxies
