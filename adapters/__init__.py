from base.types import StringEnum

from .base_adapter import BaseAdapter
from .ipfs import IPFSAdapter


class AdapterType(StringEnum):
    IPFSAdapter = IPFSAdapter.__name__
