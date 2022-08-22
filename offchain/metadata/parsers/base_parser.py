from typing import Protocol

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.models.metadata import Metadata


class BaseParser(Protocol):
    """Protocol for parsers

    Requires that a fetcher be passed into the init function.

    All parsers must implement:
    - a function for parsing metadata, given a Token and metadata info dict
    - a function that returns whether or not to run this parser, given a Token and metadata info dict
    """

    fetcher: BaseFetcher

    def __init__(self, fetcher: BaseFetcher) -> None:
        pass

    def parse_metadata(self) -> Metadata:
        pass

    def should_parse_token(self) -> bool:
        pass
