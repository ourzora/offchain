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


@ParserRegistry.register
class ENSParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.ENS]

    @staticmethod
    def make_ens_chain_name(chain_identifier: str):  # type: ignore[no-untyped-def]
        try:
            return chain_identifier.split("-")[1].lower()
        except Exception:
            logger.error(f"Received unexpected chain identifier: {chain_identifier}")
            return "mainnet"

    def get_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
        additional_fields = []
        if name_length := raw_data.get("name_length"):
            additional_fields.append(
                MetadataField(
                    field_name="name_length",
                    type=MetadataFieldType.TEXT,
                    description="Character length of ens name",
                    value=name_length,
                )
            )
        if version := raw_data.get("version"):
            additional_fields.append(
                MetadataField(
                    field_name="version",
                    type=MetadataFieldType.TEXT,
                    description="ENS NFT version",
                    value=version,
                )
            )
        if url := raw_data.get("url"):
            additional_fields.append(
                MetadataField(
                    field_name="url",
                    type=MetadataFieldType.TEXT,
                    description="ENS App URL of the name",
                    value=url,
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
                display_type=attribute_dict.get("display_type"),
            )
            for attribute_dict in attributes
        ]

    def get_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        image_uri = raw_data.get("image_url") or raw_data.get("image")
        if image_uri:
            image = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
                image.mime_type = content_type
                image.size = size
                return image
            except Exception:
                pass

    def get_background_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        bg_image_uri = raw_data.get("background_image")
        if bg_image_uri:
            image = MediaDetails(
                uri=bg_image_uri, size=None, sha256=None, mime_type=None
            )  # noqa: E501
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(bg_image_uri)
                image.mime_type = content_type
                image.size = size
                return image
            except Exception:
                pass

    def parse_metadata(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        ens_chain_name = self.make_ens_chain_name(token.chain_identifier)

        token.uri = (
            f"https://metadata.ens.domains/{ens_chain_name}/"
            f"{token.collection_address.lower()}/{token.token_id}/"
        )
        raw_data = self.fetcher.fetch_content(token.uri)  # type: ignore[assignment]
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)

        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(raw_data),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=self.get_image(raw_data=raw_data),
            content=self.get_background_image(raw_data=raw_data),
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )

    async def gen_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        image_uri = raw_data.get("image_url") or raw_data.get("image")
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

    async def gen_background_image(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[return, type-arg]  # noqa: E501
        bg_image_uri = raw_data.get("background_image")
        if bg_image_uri:
            image = MediaDetails(
                uri=bg_image_uri, size=None, sha256=None, mime_type=None
            )  # noqa: E501
            try:
                content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                    bg_image_uri
                )
                image.mime_type = content_type
                image.size = size
                return image
            except Exception as e:
                logger.error(
                    f"{self.__class__.__name__} fail to fetch background image {bg_image_uri=}. {str(e)}"
                )

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: dict, *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        ens_chain_name = self.make_ens_chain_name(token.chain_identifier)

        token.uri = (
            f"https://metadata.ens.domains/{ens_chain_name}/"
            f"{token.collection_address.lower()}/{token.token_id}/"
        )
        raw_data, mime_type_and_size = await asyncio.gather(
            self.fetcher.gen_fetch_content(token.uri),
            self.fetcher.gen_fetch_mime_type_and_size(token.uri),
        )
        mime_type, _ = mime_type_and_size
        image, background_image = await asyncio.gather(
            self.gen_image(raw_data=raw_data),
            self.gen_background_image(raw_data=raw_data),
        )
        return Metadata(
            token=token,
            raw_data=raw_data,
            attributes=self.parse_attributes(raw_data),
            name=raw_data.get("name"),
            description=raw_data.get("description"),
            mime_type=mime_type,
            image=image,
            content=background_image,
            additional_fields=self.get_additional_fields(raw_data=raw_data),
        )
