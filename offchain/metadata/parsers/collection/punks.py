import asyncio
from typing import Optional
from urllib.parse import quote

from offchain.constants.addresses import CollectionAddress
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


@ParserRegistry.register
class PunksParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.PUNKS]

    @staticmethod
    def encode_uri_data(uri: str) -> str:
        start = uri.index(",") + 1
        return quote(uri[start:])

    def make_call(self, index: int, function_sig: str) -> Optional[str]:
        results = self.contract_caller.single_address_single_fn_many_args(
            address=CollectionAddress.PUNKS_DATA,
            function_sig=function_sig,
            return_type=["string"],
            args=[[index]],
        )

        if len(results) < 1:
            return None

        return results[0]

    async def gen_call(self, index: int, function_sig: str) -> Optional[str]:
        results = await self.contract_caller.rpc.async_reader.gen_call_single_function_single_address_many_args(
            address=CollectionAddress.PUNKS_DATA,
            function_sig=function_sig,
            return_type=["string"],
            args=[[index]],
        )

        if len(results) < 1:
            return None

        return results[0]

    def get_image(self, index: int) -> Optional[MediaDetails]:
        raw_uri = self.make_call(index, "punkImageSvg(uint16)")
        image_uri = self.encode_uri_data(raw_uri)  # type: ignore[arg-type]
        return MediaDetails(
            uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml"
        )  # noqa: E501

    async def gen_image(self, index: int) -> Optional[MediaDetails]:
        raw_uri = await self.gen_call(index, "punkImageSvg(uint16)")
        image_uri = self.encode_uri_data(raw_uri)  # type: ignore[arg-type]
        return MediaDetails(
            uri=image_uri, size=None, sha256=None, mime_type="image/svg+xml"
        )  # noqa: E501

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
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
        if (title := raw_data.get("title")) is not None:
            additional_fields.append(
                MetadataField(
                    field_name="title",
                    type=MetadataFieldType.TEXT,
                    description="This property defines an the title for the NFT asset",
                    value=title,
                )
            )
        return additional_fields

    def parse_attributes(self, token_id: int) -> list[Attribute]:
        attributes = []

        punk_attributes = self.make_call(token_id, "punkAttributes(uint16)").split(", ")  # type: ignore[union-attr]  # noqa: E501

        type_attribute = Attribute(
            trait_type="Type",
            value=punk_attributes[0],
            display_type=None,
        )
        attributes.append(type_attribute)

        for value in punk_attributes[1:]:
            attribute = Attribute(
                trait_type="Accessory",
                value=value,
                display_type=None,
            )
            attributes.append(attribute)

        return attributes

    async def gen_parse_attributes(self, token_id: int) -> list[Attribute]:
        attributes = []

        punk_attributes = (await self.gen_call(token_id, "punkAttributes(uint16)")).split(", ")  # type: ignore[union-attr]  # noqa: E501

        type_attribute = Attribute(
            trait_type="Type",
            value=punk_attributes[0],
            display_type=None,
        )
        attributes.append(type_attribute)

        for value in punk_attributes[1:]:
            attribute = Attribute(
                trait_type="Accessory",
                value=value,
                display_type=None,
            )
            attributes.append(attribute)

        return attributes

    def parse_metadata(self, token: Token, *args, **kwargs) -> Metadata:  # type: ignore[no-untyped-def]  # noqa: E501
        token.uri = f"https://api.wrappedpunks.com/api/punks/metadata/{token.token_id}"
        raw_data = self.fetcher.fetch_content(token.uri)
        mime, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        image = self.get_image(token.token_id)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(token.token_id),
            name=raw_data.get("name"),  # type: ignore[union-attr]
            description=raw_data.get("description"),  # type: ignore[union-attr]
            mime_type=mime,
            image=image,
            additional_fields=self.parse_additional_fields(raw_data),  # type: ignore[arg-type]  # noqa: E501
        )

    async def _gen_parse_metadata_impl(self, token: Token, *args, **kwargs) -> Metadata:  # type: ignore[no-untyped-def]  # noqa: E501
        token.uri = f"https://api.wrappedpunks.com/api/punks/metadata/{token.token_id}"
        raw_data, mime_and_size, image, attributes = await asyncio.gather(
            self.fetcher.gen_fetch_content(token.uri),
            self.fetcher.gen_fetch_mime_type_and_size(token.uri),
            self.gen_image(token.token_id),
            self.gen_parse_attributes(token.token_id),
        )
        mime, _ = mime_and_size

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=attributes,
            name=raw_data.get("name"),  # type: ignore[union-attr]
            description=raw_data.get("description"),  # type: ignore[union-attr]
            mime_type=mime,
            image=image,
            additional_fields=self.parse_additional_fields(raw_data),  # type: ignore[arg-type]  # noqa: E501
        )
