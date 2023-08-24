from dataclasses import dataclass, field
from typing import Optional, Type, Union

import httpx
from requests.adapters import BaseAdapter as RequestsBaseAdapter
from requests.adapters import HTTPAdapter as RequestsHTTPAdapter
from urllib3.util.retry import Retry


class BaseAdapter(RequestsBaseAdapter):
    """Base Adapter inheriting from requests BaseAdapter"""

    def __init__(self, *args, **kwargs):
        super().__init__()

    async def gen_send(self, url: str, *args, **kwargs) -> httpx.Response:
        """Format and send async request to url host.

        Args:
            url (str): url to send request to

        Returns:
            httpx.Response: response from host.
        """
        raise NotImplementedError


class HTTPAdapter(RequestsHTTPAdapter):
    """HTTP Adapter inheriting from requests HTTPAdapter"""

    def __init__(
        self,
        pool_connections: int = ...,
        pool_maxsize: int = ...,
        max_retries: Union[Retry, int, None] = ...,
        pool_block: bool = ...,
        *args,
        **kwargs
    ) -> None:
        super().__init__(pool_connections, pool_maxsize, max_retries, pool_block)

    async def gen_send(self, url: str, sess: httpx.AsyncClient(), *args, **kwargs) -> httpx.Response:
        """Format and send async request to url host.

        Args:
            url (str): url to send request to

        Returns:
            httpx.Response: response from host.
        """
        return await sess.get(url, follow_redirects=True)


Adapter = Union[BaseAdapter, HTTPAdapter]


@dataclass
class AdapterConfig:
    adapter_cls: Type[Adapter]
    mount_prefixes: list[str]
    host_prefixes: Optional[list[str]] = None
    kwargs: dict = field(default_factory=dict)
