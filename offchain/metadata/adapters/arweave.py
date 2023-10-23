import random
from typing import Optional

import httpx
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
        self.host_prefixes = host_prefixes or ["https://arweave.net/"]

        assert all(
            [g.endswith("/") for g in self.host_prefixes]
        ), "gateways should have trailing slashes"

        self.key = key
        self.secret = secret
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def parse_ar_url(self, url: str) -> str:
        """Format and send async request to ARWeave host.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client

        Returns:
            httpx.Response: response from ARWeave host.
        """
        parsed = parse_url(url)
        if parsed.scheme == "ar":
            gateway = random.choice(self.host_prefixes)
            new_url = f"{gateway}{parsed.host}"
            if parsed.path is not None:
                new_url += parsed.path
            url = new_url
        return url

    async def gen_send(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def, valid-type]  # noqa: E501
        """Format and send an async `GET` request to ARWeave host at parsed url.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client

        Returns:
            httpx.Response: response from ARWeave host.
        """
        return await sess.get(self.parse_ar_url(url), timeout=self.timeout, follow_redirects=True)  # type: ignore[no-any-return]  # noqa: E501

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:  # type: ignore[no-untyped-def]  # noqa: E501
        """Format and send a `GET` request to ARWeave host at parsed url.

        Args:
            request (PreparedRequest): incoming request

        Returns:
            Response: response from ARWeave host.
        """
        request.url = self.parse_ar_url(request.url)  # type: ignore[arg-type]
        kwargs["timeout"] = self.timeout
        return super().send(request, *args, **kwargs)

    async def gen_head(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def, valid-type]  # noqa: E501
        """Format and send an async `HEAD` request to ARWeave host at parsed url.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client

        Returns:
            httpx.Response: response from ARWeave host.
        """
        return await sess.head(self.parse_ar_url(url), timeout=self.timeout, follow_redirects=True)  # type: ignore[no-any-return]  # noqa: E501
