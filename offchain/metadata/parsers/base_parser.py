from abc import abstractmethod
from typing import Optional, Protocol

import pytest

from offchain.logger.logging import logger
from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.models.metadata import Metadata, MetadataStandard
from offchain.metadata.models.token import Token


class BaseParser(Protocol):
    """Base protocol for Parser classes

    Attributes:
        _METADATA_STANDARD (MetadataStandard): a class variable defining the metadata standard a parser supports.
        fetcher (BaseFetcher): a fetcher instance responsible for fetching content,
            mime type, and size by making requests.
    """  # noqa: E501

    _METADATA_STANDARD: MetadataStandard

    fetcher: BaseFetcher

    def __init__(self, fetcher: BaseFetcher) -> None:
        pass

    def parse_metadata(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: dict, *args, **kwargs  # type: ignore[type-arg]
    ) -> Optional[Metadata]:
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """  # noqa: E501
        pass

    def should_parse_token(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: Optional[dict], *args, **kwargs  # type: ignore[type-arg]  # noqa: E501
    ) -> bool:
        """Return whether or not a collection parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.
            raw_data (dict): raw data returned from token uri.

        Returns:
            bool: whether or not the collection parser handles this token.
        """
        pass

    @abstractmethod
    async def _gen_parse_metadata_impl(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: dict, *args, **kwargs  # type: ignore[type-arg]
    ):
        raise NotImplementedError("Not implemented")

    async def gen_parse_metadata(  # type: ignore[no-untyped-def]
        self, token: Token, raw_data: dict, *args, **kwargs  # type: ignore[type-arg]
    ) -> Optional[Metadata]:
        """Given a token and raw data returned from the token uri, return a normalized Metadata object.

        Args:
            token (Token): token to process metadata for.
            raw_data (dict): raw data returned from token uri.

        Returns:
            Optional[Metadata]: normalized metadata object, if successfully parsed.
        """  # noqa: E501
        try:
            return await self._gen_parse_metadata_impl(token, raw_data, *args, **kwargs)  # type: ignore[no-any-return]  # noqa: E501
        except NotImplementedError:
            logger.warn(
                f"{self.__class__.__name__} doesn't implement gen_parse_metadata, fallback to legacy parse_metadata"  # noqa: E501
            )
            if pytest.is_running:
                raise
            return self.parse_metadata(token, raw_data, *args, **kwargs)
