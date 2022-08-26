from offchain.metadata.fetchers import BaseFetcher
from offchain.metadata.parsers.base_parser import BaseParser
from offchain.metadata.models.token import Token
from offchain.metadata.web3.batching import BatchContractViewCaller


class CollectionParser(BaseParser):
    _COLLECTION_ADDRESSES: list[str]

    def __init__(self, fetcher: BaseFetcher, contract_caller: BatchContractViewCaller, *args, **kwargs) -> None:
        self.contract_caller = contract_caller
        self.fetcher = fetcher

    def should_parse_token(self, token: Token, *args, **kwargs) -> bool:
        return token.collection_address in self._COLLECTION_ADDRESSES
