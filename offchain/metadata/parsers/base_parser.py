from typing import Optional, Protocol

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.models.metadata import Metadata, MetadataStandard
from offchain.metadata.models.token import Token


class BaseParser(Protocol):
    """Base protocol for Parser classes

    Attributes:
        _METADATA_STANDARD (MetadataStandard): a class variable defining the metadata standard a parser supports.
        fetcher (BaseFetcher): a fetcher instance responsible for fetching content,
            mime type, and size by making requests.
    """

    _METADATA_STANDARD: MetadataStandard

    fetcher: BaseFetcher

    def __init__(self, fetcher: BaseFetcher) -> None:
        pass

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """
        pass

    def should_parse_token(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> bool:
        """Return whether or not a collection parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.
            raw_data (dict): raw data returned from token uri.

        Returns:
            bool: whether or not the collection parser handles this token.
        """
        pass
