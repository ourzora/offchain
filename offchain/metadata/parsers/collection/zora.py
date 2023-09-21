import asyncio
from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.logger.logging import logger
from offchain.metadata.models.metadata import (
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.catchall.default_catchall import DefaultCatchallParser
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.ZORA_MEDIA


@ParserRegistry.register
class ZoraParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
        additional_fields = []
        if version := raw_data.get("version"):
            additional_fields.append(
                MetadataField(
                    field_name="version",
                    type=MetadataFieldType.TEXT,
                    description="Zora Metadata version",
                    value=version,
                )
            )

        return additional_fields

    def get_uri(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            ADDRESS,
            function_sig="tokenMetadataURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    async def gen_uri(self, token_id: int) -> Optional[str]:
        results = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            ADDRESS,
            function_sig="tokenMetadataURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_content_uri(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    async def gen_content_uri(self, token_id: int) -> Optional[str]:
        results = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            ADDRESS,
            function_sig="tokenURI(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_content_details(self, uri: str) -> Optional[MediaDetails]:
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(uri)
            return MediaDetails(uri=uri, size=size, sha256=None, mime_type=content_type)
        except Exception:
            pass

        return None

    async def gen_content_details(self, uri: str) -> Optional[MediaDetails]:
        try:
            content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(uri)
            return MediaDetails(uri=uri, size=size, sha256=None, mime_type=content_type)
        except Exception as e:
            logger.error(f"{self.__class__.__name__} fail to content {uri=}. {str(e)}")

        return None

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        if token.uri is None or raw_data is None or not isinstance(raw_data, dict):
            token.uri = self.get_uri(token.token_id)
            raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[arg-type, assignment]  # noqa: E501

        metadata = DefaultCatchallParser(self.fetcher).parse_metadata(token=token, raw_data=raw_data)  # type: ignore[arg-type]  # noqa: E501

        content_uri = self.get_content_uri(token.token_id)
        content = self.get_content_details(content_uri)  # type: ignore[arg-type]

        # if we have an image, make sure we set
        # the image field, otherwise fallback to content
        if content.mime_type.startswith("image"):  # type: ignore[union-attr]
            metadata.image = content  # type: ignore[union-attr]
        else:
            metadata.content = content  # type: ignore[union-attr]

        metadata.additional_fields = self.parse_additional_fields(raw_data)  # type: ignore[arg-type, union-attr]  # noqa: E501
        metadata.mime_type = "application/json"  # type: ignore[union-attr]

        return metadata

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        if token.uri is None:
            token.uri = await self.gen_uri(token.token_id)
        if raw_data is None or not isinstance(raw_data, dict):
            raw_data = await self.fetcher.gen_fetch_content(  # type:ignore[assignment]
                token.uri  # type:ignore[arg-type]
            )

        metadata, content_uri = await asyncio.gather(
            DefaultCatchallParser(self.fetcher).gen_parse_metadata(token=token, raw_data=raw_data),  # type: ignore[arg-type]  # noqa: E501
            self.gen_content_uri(token.token_id),
        )
        content = await self.gen_content_details(content_uri)  # type: ignore[arg-type]

        # if we have an image, make sure we set
        # the image field, otherwise fallback to content
        if content.mime_type.startswith("image"):  # type: ignore[union-attr]
            metadata.image = content  # type: ignore[union-attr]
        else:
            metadata.content = content  # type: ignore[union-attr]

        metadata.additional_fields = self.parse_additional_fields(raw_data)  # type: ignore[arg-type, union-attr]  # noqa: E501
        metadata.mime_type = "application/json"  # type: ignore[union-attr]

        return metadata
