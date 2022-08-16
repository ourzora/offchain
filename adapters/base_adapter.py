from typing import Union

from requests.adapters import BaseAdapter, HTTPAdapter

Adapter = Union[BaseAdapter, HTTPAdapter]
