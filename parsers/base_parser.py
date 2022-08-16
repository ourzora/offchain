from typing import Protocol

from fetchers.base_fetcher import BaseFetcher
from models.metadata import Metadata


class BaseParser(Protocol):
    fetcher: BaseFetcher

    def __init__(self, fetcher: BaseFetcher) -> None:
        pass

    def parse_metadata(self) -> Metadata:
        pass
