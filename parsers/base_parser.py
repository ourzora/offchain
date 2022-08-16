from typing import Protocol

from metazerse.fetchers.base_fetcher import BaseFetcher
from metazerse.models.metadata import Metadata


class BaseParser(Protocol):
    fetcher: BaseFetcher

    def __init__(self, fetcher: BaseFetcher) -> None:
        pass

    def parse_metadata(self) -> Metadata:
        pass
