from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.models.metadata import MetadataStandard
from offchain.metadata.parsers.base_parser import BaseParser


class CatchallParser(BaseParser):
    """Base class for catchall parsers

    Catchall parsers are parsers that handle parsing metadata that don't neatly fall into a specific schema shape.
    """

    _METADATA_STANDARD: MetadataStandard = MetadataStandard.UNKNOWN_STANDARD

    def __init__(self, fetcher: BaseFetcher, *args, **kwargs) -> None:
        self.fetcher = fetcher
