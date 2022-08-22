import random
from typing import Optional
from requests import PreparedRequest, Response
from urllib3.util import parse_url

from offchain.metadata.adapters.base_adapter import HTTPAdapter
from offchain.metadata.registries.adapter_registry import AdapterRegistry


@AdapterRegistry.register
class ARWeaveAdapter(HTTPAdapter):
    """Requests adapter for making requests to Arweave"""

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
        """For IPFS hashes, query pinata cloud gateway

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: response from IPFS Gateway
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
