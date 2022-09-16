from dataclasses import dataclass, field
from typing import Optional, Type, Union

from requests.adapters import (
    BaseAdapter as RequestsBaseAdapter,
    HTTPAdapter as RequestsHTTPAdapter,
)
from urllib3.util.retry import Retry


class BaseAdapter(RequestsBaseAdapter):
    """Base Adapter inheriting from requests BaseAdapter"""

    def __init__(self, *args, **kwargs):
        super().__init__()


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


Adapter = Union[BaseAdapter, HTTPAdapter]


@dataclass
class AdapterConfig:
    adapter_cls: Type[Adapter]
    mount_prefixes: list[str]
    host_prefixes: Optional[list[str]] = None
    kwargs: dict = field(default_factory=dict)
