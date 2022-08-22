from offchain.constants.addresses import CollectionAddress
from offchain.metadata.fetchers import BaseFetcher
from offchain.metadata.models.metadata import Metadata
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class NounsParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [
        CollectionAddress.NOUNS,
        CollectionAddress.LIL_NOUNS,
    ]

    def __init__(self, fetcher: BaseFetcher) -> None:
        super().__init__(fetcher)

    def parse_metadata(self) -> Metadata:
        return super().parse_metadata()

    def should_parse_token(self, token: Token, *args, **kwargs) -> bool:
        return super().should_parse_token(token, *args, **kwargs)
