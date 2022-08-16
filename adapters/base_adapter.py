from typing import Union

from requests.adapters import BaseAdapter as RequestsBaseAdapter
from requests.adapters import HTTPAdapter as RequestsHTTPAdapter


class BaseAdapter(RequestsBaseAdapter):
    pass


class HTTPAdapter(RequestsHTTPAdapter):
    pass


Adapter = Union[BaseAdapter, HTTPAdapter]
