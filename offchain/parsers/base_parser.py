from typing import Protocol

from offchain.fetchers.base_fetcher import BaseFetcher
from offchain.models.metadata import Metadata


class BaseParser(Protocol):
    fetcher: BaseFetcher

    def __init__(self, fetcher: BaseFetcher) -> None:
        pass

    def parse_metadata(self) -> Metadata:
        pass

    def should_parse_token(self) -> bool:
        pass
