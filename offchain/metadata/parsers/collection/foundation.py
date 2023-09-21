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

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        if token.uri is None or raw_data is None:
            token.uri = f"https://api.foundation.app/opensea/{token.token_id}"
            raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[assignment]
        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)  # type: ignore[arg-type]  # noqa: E501
        metadata.standard = None  # type: ignore[union-attr]
        if metadata.content.uri.endswith("glb"):  # type: ignore[union-attr]
            metadata.content.mime_type = "model/gltf-binary"  # type: ignore[union-attr]

        return metadata

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        if token.uri is None or raw_data is None:
            token.uri = f"https://api.foundation.app/opensea/{token.token_id}"
            raw_data = await self.fetcher.gen_fetch_content(token.uri)  # type: ignore[assignment]
        metadata = await DefaultCatchallParser(self.fetcher).gen_parse_metadata(token=token, raw_data=raw_data)  # type: ignore[arg-type]  # noqa: E501
        metadata.standard = None  # type: ignore[union-attr]
        if metadata.content.uri.endswith("glb"):  # type: ignore[union-attr]
            metadata.content.mime_type = "model/gltf-binary"  # type: ignore[union-attr]

        return metadata
