from typing import Optional, Protocol

from offchain.fetchers.base_fetcher import BaseFetcher
from offchain.parsers.base_parser import BaseParser


class BasePipeline(Protocol):
    fetcher: Optional[BaseFetcher]
    parsers: Optional[list[BaseParser]]

    def __init__(
        self,
        fetcher: Optional[BaseFetcher],
        parsers: Optional[list[BaseParser]],
    ) -> None:
        pass

    def mount_adapter(self):
        pass

    def run(self):
        pass
