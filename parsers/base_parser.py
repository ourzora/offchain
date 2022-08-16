from metazerse.fetchers.base_fetcher import BaseFetcher
from metazerse.models.metadata import Metadata


class BaseParser:
    def __init__(self, fetcher: BaseFetcher) -> None:
        self.fetcher = fetcher

    def parse_metadata() -> Metadata:
        raise NotImplementedError
