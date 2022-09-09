import random
from typing import Optional
from requests import PreparedRequest, Response
from urllib3.util import parse_url

from offchain.metadata.adapters.base_adapter import HTTPAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class ARWeaveAdapter(HTTPAdapter):
    """Provides an interface for Requests sessions to contact ARWeave urls.

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

        self.host_prefixes = host_prefixes or ["https://arweave.net/"]

        assert all([g.endswith("/") for g in self.host_prefixes]), "gateways should have trailing slashes"

        self.key = key
        self.secret = secret
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        """Format and send request to ARWeave host.

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: response from ARWeave host.
        """
        parsed = parse_url(request.url)
        if parsed.scheme == "ar":
            gateway = random.choice(self.host_prefixes)
            url = f"{gateway}{parsed.host}"
            if parsed.path is not None:
                url += parsed.path
            request.url = url
        kwargs["timeout"] = self.timeout
        return super().send(request, *args, **kwargs)
