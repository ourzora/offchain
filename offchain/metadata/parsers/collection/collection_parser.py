from offchain.metadata.fetchers import BaseFetcher
from offchain.metadata.parsers.base_parser import BaseParser
from offchain.metadata.models.token import Token
from offchain.metadata.web3.batching import BatchContractViewCaller


class CollectionParser(BaseParser):
    """Base class for collection parsers

    All parsers that handle collection-based metadata parsing will need to
    inherit from this base class.

    Attributes:
        _COLLECTION_ADDRESSES (list[str]): list of collection addresses that a parser class handles.
    """

    _COLLECTION_ADDRESSES: list[str]

    def __init__(self, fetcher: BaseFetcher, contract_caller: BatchContractViewCaller, *args, **kwargs) -> None:
        self.contract_caller = contract_caller
        self.fetcher = fetcher

    def should_parse_token(self, token: Token, *args, **kwargs) -> bool:
        """Return whether or not a collection parser should parse a given token.

        Args:
            token (Token): the token whose metadata needs to be parsed.

        Returns:
            bool: whether or not the collection parser handles this token.
        """
        return token.collection_address in self._COLLECTION_ADDRESSES
