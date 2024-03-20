from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.metadata.models.metadata import Metadata
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class FoundationParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.FOUNDATION]

    def _normalize_metadata(self, metadata: Optional[Metadata]) -> Optional[Metadata]:
        if metadata is None:
            return None

        metadata.standard = None  # type: ignore[union-attr]
        if (
            metadata
            and metadata.image
            and metadata.image.uri
            and metadata.image.uri.endswith("glb")
        ):
            metadata.image.mime_type = "model/gltf-binary"

        return metadata

    def parse_metadata(
        self, token: Token, raw_data: Optional[dict], *args, **kwargs
    ) -> Optional[Metadata]:
        if token.uri is None or raw_data is None:
            token.uri = self.contract_caller.single_address_single_fn_many_args(
                token.collection_address,
                "tokenURI(uint256)",
                ["string"],
                [[token.token_id]],
            )[0]
            if token.uri is None:
                return None

            content = self.fetcher.fetch_content(token.uri)
            if content and isinstance(content, dict):
                raw_data = content

        if raw_data is None:
            return None

        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(
            token=token, raw_data=raw_data
        )

        return self._normalize_metadata(metadata)

    async def _gen_parse_metadata_impl(
        self, token: Token, raw_data: Optional[dict], *args, **kwargs
    ) -> Optional[Metadata]:
        if token.uri is None or raw_data is None:
            token.uri = await self.contract_caller.rpc.async_reader.call_function(
                token.collection_address,
                "tokenURI(uint256)",
                ["string"],
                [token.token_id],
            )
            if token.uri is None:
                return None

            content = await self.fetcher.gen_fetch_content(token.uri)
            if content and isinstance(content, dict):
                raw_data = content

        if raw_data is None:
            return None

        metadata = await DefaultCatchallParser(self.fetcher).gen_parse_metadata(
            token=token, raw_data=raw_data
        )

        return self._normalize_metadata(metadata)
