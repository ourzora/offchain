from base.types import StringEnum

from .base_fetcher import BaseFetcher
from .metadata_fetcher import MetadataFetcher


class FetcherType(StringEnum):
    MetadataFetcher = MetadataFetcher.__name__
