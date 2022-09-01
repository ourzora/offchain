from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import Metadata
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.CHAINRUNNERS


@ParserRegistry.register
class ChainRunnersParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.CHAINRUNNERS]

    def get_dna(self, token_id: int) -> Optional[int]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=ADDRESS,
            function_sig="getDna(uint256)",
            return_type=["uint256"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:
        if token.uri is None or raw_data is None:
            dna = self.get_dna(token.token_id)
            token.uri = f"https://api.chainrunners.xyz/tokens/metadata/{token.token_id}?dna={dna}"
            raw_data = self.fetcher.fetch_content(token.uri)

        return DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)
