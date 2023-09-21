from typing import Optional

from offchain.metadata.fetchers.base_fetcher import BaseFetcher
from offchain.metadata.fetchers.metadata_fetcher import MetadataFetcher
from offchain.metadata.models.metadata import MetadataStandard
from offchain.metadata.parsers.base_parser import BaseParser
from offchain.metadata.models.token import Token
from offchain.web3.contract_caller import ContractCaller


class CollectionParser(BaseParser):
    """Base class for collection parsers

    All parsers that handle collection-based metadata parsing will need to
    inherit from this base class.

    Attributes:
        _COLLECTION_ADDRESSES (list[str]): list of collection addresses that a parser class handles.
        _METADATA_STANDARD: (MetadataStandard): metadata standard of all metadata returned by this class of parser.
            Defaults to MetadataStandard.COLLECTION_STANDARD.
        fetcher (BaseFetcher, optional): a fetcher instance for making network requests.
        contract_caller (ContractCaller, optional): a contract caller instance for fetching data from contracts.
    """  # noqa: E501

    _COLLECTION_ADDRESSES: list[str]
    _METADATA_STANDARD: MetadataStandard = MetadataStandard.COLLECTION_STANDARD

    def __init__(  # type: ignore[no-untyped-def]
        self,
        fetcher: Optional[BaseFetcher] = None,
        contract_caller: Optional[ContractCaller] = None,
        *args,
        **kwargs  # noqa: E501
    ) -> None:
        self.contract_caller = contract_caller or ContractCaller()
        self.fetcher = fetcher or MetadataFetcher()

    def should_parse_token(self, token: Token, *args, **kwargs) -> bool:  # type: ignore[no-untyped-def]  # noqa: E501
        """Return whether or not a collection parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.

        Returns:
            bool: whether or not the collection parser handles this token.
        """
        return token.collection_address.lower() in [
            address.lower() for address in self._COLLECTION_ADDRESSES
        ]  # noqa: E501
