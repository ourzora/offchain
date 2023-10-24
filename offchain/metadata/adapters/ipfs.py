import random
from typing import Optional

import httpx
from requests import PreparedRequest, Response
from urllib3.util import parse_url

from offchain.metadata.adapters.base_adapter import HTTPAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


def build_request_url(gateway: str, request_url: str) -> str:
    """Parse and format incoming IPFS request url

    Args:
        gateway (str): gateway to use when making a request
        request_url (str): incoming IPFS request url

    Returns:
        str: formatted IPFS url
    """

    parsed_url = parse_url(request_url)
    url = f"{gateway}"
    # Handle "ipfs://" prefixed urls
    if parsed_url.scheme == "ipfs":
        # Don't duplicate since gateways already have "ipfs/"
        if parsed_url.host != "ipfs":
            host = parsed_url.host
            # Remove duplicate slashes
            if url.endswith("/") and host.startswith("/"):  # type: ignore[union-attr]
                host = host[1:]  # type: ignore[index]
            url += host  # type: ignore[operator]
        if parsed_url.path is not None:
            path = parsed_url.path
            # Remove duplicate slashes
            if url.endswith("/") and path.startswith("/"):
                path = path[1:]
            url += path
    # Handle "https://" prefixed urls that have "/ipfs/" in the path
    elif parsed_url.scheme == "https" and "ipfs" in parsed_url.path:  # type: ignore[operator]  # noqa: E501
        url = f"{gateway}"
        if parsed_url.path is not None:
            path = parsed_url.path
            # Remove duplicate slashes
            if url.endswith("/") and path.startswith("/"):
                path = path[1:]
            if path.startswith("ipfs/"):
                path = path[5:]
            url += path
    return url


@AdapterRegistry.register
class IPFSAdapter(HTTPAdapter):
    """Provides an interface for Requests sessions to contact IPFS urls.

    Args:
        host_prefixes (list[str], optional): list of possible host url prefixes to choose from
        key (str, optional): optional key to send with request
        secret (str, optional): optional secret to send with request
        timeout (int): request timeout in seconds. Defaults to 10 seconds.
    """  # noqa: E501

    def __init__(  # type: ignore[no-untyped-def]
        self,
        host_prefixes: Optional[list[str]] = None,
        key: Optional[str] = None,
        secret: Optional[str] = None,
        timeout: int = 10,
        *args,
        **kwargs,
    ):
        self.host_prefixes = host_prefixes or ["https://gateway.pinata.cloud/ipfs/"]

        assert all(
            [g.endswith("/") for g in self.host_prefixes]
        ), "gateways should have trailing slashes"

        self.key = key
        self.secret = secret
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def make_request_url(self, request_url: str, gateway: Optional[str] = None) -> str:
        """Parse and format incoming IPFS request url

        Args:
            request_url (str): incoming IPFS request url
            gateway (Optional[str]): gateway to use when making a request

        Returns:
            str: formatted IPFS url
        """

        gateway = gateway or random.choice(self.host_prefixes)
        return build_request_url(gateway=gateway, request_url=request_url)

    async def gen_send(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def, valid-type]  # noqa: E501
        """Format and send an async `GET` request to IPFS host.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client session

        Returns:
            httpx.Response: response from IPFS host.
        """
        return await sess.get(self.make_request_url(url), timeout=self.timeout, follow_redirects=True)  # type: ignore[no-any-return]  # noqa: E501

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:  # type: ignore[no-untyped-def]  # noqa: E501
        """For IPFS hashes, query pinata cloud gateway

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: response from IPFS Gateway
        """
        request.url = self.make_request_url(request.url)  # type: ignore[arg-type]

        kwargs["timeout"] = self.timeout
        return super().send(request, *args, **kwargs)

    async def gen_head(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def, valid-type]  # noqa: E501
        """Format and send an async `HEAD` request to IPFS host.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client session

        Returns:
            httpx.Response: response from IPFS host.
        """
        return await sess.head(self.make_request_url(url), timeout=self.timeout, follow_redirects=True)  # type: ignore[no-any-return]  # noqa: E501
