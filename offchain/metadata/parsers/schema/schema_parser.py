from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.parsers.base_parser import BaseParser


class SchemaParser(BaseParser):
    """Base class for schema parsers

    All parsers that handle schema-based metadata parsing will need to inherit from this base class.
    """

    def __init__(self, fetcher: BaseFetcher, *args, **kwargs) -> None:
        self.fetcher = fetcher
