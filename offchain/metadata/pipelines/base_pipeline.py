from typing import Optional, Protocol

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.parsers.base_parser import BaseParser


class BasePipeline(Protocol):
    """Protocol for pipelines

    Requires that a fetcher and list of parsers be passed into the init function

    All pipelines must implement:
    - a function for mounting an adapter to a list of url prefixes
    - a function that processes metadata for a list of tokens

    """

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
