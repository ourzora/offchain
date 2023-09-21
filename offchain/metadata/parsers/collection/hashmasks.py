import asyncio
from typing import Optional

from offchain.constants.addresses import CollectionAddress
from offchain.logger.logging import logger
from offchain.metadata.models.metadata import (
    Attribute,
    MediaDetails,
    Metadata,
    MetadataField,
    MetadataFieldType,
)
from offchain.metadata.models.token import Token
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry

ADDRESS = CollectionAddress.HASHMASKS


@ParserRegistry.register
class HashmasksParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [ADDRESS]

    def get_name(self, token_id: int) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=ADDRESS,
            function_sig="tokenNameByIndex(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    async def gen_name(self, token_id: int) -> Optional[str]:
        results = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            address=ADDRESS,
            function_sig="tokenNameByIndex(uint256)",
            return_type=["string"],
            args=[[token_id]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
        additional_fields = []
        if (external_url := raw_data.get("external_url")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="external_url",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an optional external URL that can reference a webpage or "  # noqa: E501
                    "external asset for the NFT",
                    value=external_url,
                )
            )
        return additional_fields

    def parse_attributes(self, raw_data: dict) -> Optional[list[Attribute]]:  # type: ignore[type-arg]  # noqa: E501
        attributes = raw_data.get("attributes")
        if not attributes or not isinstance(attributes, list):
            return  # type: ignore[return-value]

        return [
            Attribute(
                trait_type=attribute_dict.get("trait_type"),
                value=attribute_dict.get("value"),
                display_type=None,
            )
            for attribute_dict in attributes
        ]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        image_uri = raw_data.get("image")
        if image_uri:
            image = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
                image.mime_type = content_type
                image.size = size
                return image
            except Exception:
                pass

    async def gen_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        image_uri = raw_data.get("image")
        if image_uri:
            image = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                    image_uri
                )
                image.mime_type = content_type
                image.size = size
                return image
            except Exception as e:
                logger.error(
                    f"{self.__class__.__name__} fail to fetch image {image_uri=}. {str(e)}"
                )

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        token.uri = f"https://hashmap.azurewebsites.net/getMask/{token.token_id}"

        raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[assignment]
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(raw_data) or [],
            name=self.get_name(token.token_id),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        token.uri = f"https://hashmap.azurewebsites.net/getMask/{token.token_id}"

        raw_data, mime_type_and_size, name, image = await asyncio.gather(
            self.fetcher.gen_fetch_content(token.uri),
            self.fetcher.gen_fetch_mime_type_and_size(token.uri),
            self.gen_name(token.token_id),
            self.gen_image(raw_data=raw_data),
        )
        mime_type, _ = mime_type_and_size

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(raw_data) or [],
            name=name,
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=image,
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )
