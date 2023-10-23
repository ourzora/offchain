from dataclasses import dataclass, field
from typing import Optional, Type, Union

import httpx
from requests.adapters import BaseAdapter as RequestsBaseAdapter
from requests.adapters import HTTPAdapter as RequestsHTTPAdapter
from urllib3.util.retry import Retry


class BaseAdapter(RequestsBaseAdapter):
    """Base Adapter inheriting from requests BaseAdapter"""

    def __init__(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        super().__init__()

    async def gen_send(self, url: str, *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def]  # noqa: E501
        """
        Format and send an async `GET` request to url host.
        Abstract method, implemented in subclasses.

        Args:
            url (str): url to send request to

        Returns:
            httpx.Response: response from host.
        """
        raise NotImplementedError

    async def gen_head(self, url: str, *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def]  # noqa: E501
        """
        Format and send an async `HEAD` request to url host.
        Abstract method, implemented in subclasses.

        Args:
            url (str): url to send request to

        Returns:
            httpx.Response: response from host.
        """
        raise NotImplementedError


class HTTPAdapter(RequestsHTTPAdapter):
    """HTTP Adapter inheriting from requests HTTPAdapter"""

    def __init__(  # type: ignore[no-untyped-def]
        self,
        pool_connections: int = ...,  # type: ignore[assignment]
        pool_maxsize: int = ...,  # type: ignore[assignment]
        max_retries: Union[Retry, int, None] = ...,  # type: ignore[assignment]
        pool_block: bool = ...,  # type: ignore[assignment]
        *args,
        **kwargs
    ) -> None:
        super().__init__(pool_connections, pool_maxsize, max_retries, pool_block)

    async def gen_send(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def, valid-type]  # noqa: E501
        """Format and send an async `GET` request to url host.

        Args:
            url (str): url to send request to

        Returns:
            httpx.Response: response from host.
        """
        return await sess.get(url, follow_redirects=True)  # type: ignore[no-any-return]

    async def gen_head(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:  # type: ignore[no-untyped-def, valid-type]  # noqa: E501
        """Format and send an async `HEAD` request to url host.

        Args:
            url (str): url to send request to
            sess (httpx.AsyncClient()): async client

        Returns:
            httpx.Response: response from host.
        """
        return await sess.head(url, follow_redirects=True)  # type: ignore[no-any-return]


Adapter = Union[BaseAdapter, HTTPAdapter]


@dataclass
class AdapterConfig:
    adapter_cls: Type[Adapter]
    mount_prefixes: list[str]
    host_prefixes: Optional[list[str]] = None
    kwargs: dict = field(default_factory=dict)  # type: ignore[type-arg]
