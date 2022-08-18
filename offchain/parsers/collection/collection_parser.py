from offchain.parsers.base_parser import BaseParser
from offchain.models.token import Token


class CollectionParser(BaseParser):
    _COLLECTION_ADDRESSES: list[str]

    def should_parse_token(self, token: Token, *args, **kwargs) -> bool:
        return token.collection_address in self._COLLECTION_ADDRESSES
