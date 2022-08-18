from offchain.base.types import StringEnum

from .arweave import ARWeaveAdapter
from .base_adapter import BaseAdapter
from .data_uri import DataURIAdapter
from .http_adapter import HTTPAdapter
from .ipfs import IPFSAdapter


class AdapterType(StringEnum):
    ARWeaveAdapter = ARWeaveAdapter.__name__
    DataURIAdapter = DataURIAdapter.__name__
    HTTPAdapter = HTTPAdapter.__name__
    IPFSAdapter = IPFSAdapter.__name__
