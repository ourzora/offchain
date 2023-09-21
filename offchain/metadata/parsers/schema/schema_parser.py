from typing import Optional

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.parsers.base_parser import BaseParser


class SchemaParser(BaseParser):
    """Base class for schema parsers

    All parsers that handle schema-based metadata parsing will need to inherit from this base class.

    Attributes:
        fetcher (BaseFetcher, optional): a fetcher instance for making network requests
    """  # noqa: E501

    def __init__(self, fetcher: Optional[BaseFetcher] = None, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]  # noqa: E501
        self.fetcher = fetcher or MetadataFetcher()
