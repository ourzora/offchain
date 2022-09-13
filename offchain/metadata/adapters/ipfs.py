import random
from requests import PreparedRequest, Response
from typing import Optional
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
            if url.endswith("/") and host.startswith("/"):
                host = host[1:]
            url += host
        if parsed_url.path is not None:
            path = parsed_url.path
            # Remove duplicate slashes
            if url.endswith("/") and path.startswith("/"):
                path = path[1:]
            url += path
    # Handle "https://" prefixed urls that have "/ipfs/" in the path
    elif parsed_url.scheme == "https" and "ipfs" in parsed_url.path:
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
    """

    def __init__(
        self,
        host_prefixes: Optional[list[str]] = None,
        key: Optional[str] = None,
        secret: Optional[str] = None,
        timeout: int = 10,
        *args,
        **kwargs,
    ):

        self.host_prefixes = host_prefixes or ["https://gateway.pinata.cloud/ipfs/"]

        assert all([g.endswith("/") for g in self.host_prefixes]), "gateways should have trailing slashes"

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

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        """For IPFS hashes, query pinata cloud gateway

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: response from IPFS Gateway
        """
        request.url = self.make_request_url(request.url)

        kwargs["timeout"] = self.timeout
        return super().send(request, *args, **kwargs)
