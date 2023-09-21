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
from offchain.metadata.parsers.collection.collection_parser import CollectionParser
from offchain.metadata.registries.parser_registry import ParserRegistry


@ParserRegistry.register
class SuperRareParser(CollectionParser):
    _COLLECTION_ADDRESSES: list[str] = [CollectionAddress.SUPERRARE]

    def get_image_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        image_uri = raw_data.get("image")
        if not image_uri:
            return None
        details = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = self.fetcher.fetch_mime_type_and_size(image_uri)
            details.mime_type = content_type
            details.size = size
        except Exception:
            pass
        return details

    async def gen_image_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        image_uri = raw_data.get("image")
        if not image_uri:
            return None
        details = MediaDetails(uri=image_uri, size=None, sha256=None, mime_type=None)
        try:
            content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                image_uri
            )
            details.mime_type = content_type
            details.size = size
        except Exception as e:
            logger.error(
                f"{self.__class__.__name__} fail to fetch image {image_uri=}. {str(e)}"
            )
        return details

    def get_content_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        media = raw_data.get("media")
        if not media or not isinstance(media, dict):
            return  # type: ignore[return-value]
        content_uri = media.get("uri")
        if not content_uri:
            return  # type: ignore[return-value]
        details = MediaDetails(
            uri=content_uri,
            size=media.get("size"),
            sha256=None,
            mime_type=media.get("mimeType"),
        )
        if not details.mime_type:
            try:
                content_type, size = self.fetcher.fetch_mime_type_and_size(content_uri)
                details.mime_type = content_type
                details.size = size
            except Exception:
                pass

        return details

    async def gen_content_details(self, raw_data: dict) -> Optional[MediaDetails]:  # type: ignore[type-arg]  # noqa: E501
        media = raw_data.get("media")
        if not media or not isinstance(media, dict):
            return  # type: ignore[return-value]
        content_uri = media.get("uri")
        if not content_uri:
            return  # type: ignore[return-value]
        details = MediaDetails(
            uri=content_uri,
            size=media.get("size"),
            sha256=None,
            mime_type=media.get("mimeType"),
        )
        if not details.mime_type:
            try:
                content_type, size = await self.fetcher.gen_fetch_mime_type_and_size(
                    content_uri
                )
                details.mime_type = content_type
                details.size = size
            except Exception as e:
                logger.error(
                    f"{self.__class__.__name__} fail to fetch content type and size "
                    f"{content_uri=}. {str(e)}"
                )

        return details

    def parse_additional_fields(self, raw_data: dict) -> list[MetadataField]:  # type: ignore[type-arg]  # noqa: E501
        additional_fields = []
        if created_by := raw_data.get("createdBy"):
            additional_fields.append(
                MetadataField(
                    field_name="created_by",
                    type=MetadataFieldType.TEXT,
                    description="The creator of an NFT.",
                    value=created_by,
                )
            )
        if year_created := raw_data.get("yearCreated"):
            additional_fields.append(
                MetadataField(
                    field_name="year_created",
                    type=MetadataFieldType.NUMBER,
                    description="The year in which an NFT was created.",
                    value=year_created,
                )
            )
        if tags := raw_data.get("tags"):
            additional_fields.append(
                MetadataField(
                    field_name="tags",
                    type=MetadataFieldType.LIST,
                    description="List of tags associated with an NFT.",
                    value=tags,
                )
            )
        return additional_fields

    def parse_metadata(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        mime_type, _ = self.fetcher.fetch_mime_type_and_size(token.uri)  # type: ignore[arg-type]  # noqa: E501

        return Metadata(
            token=token,
            raw_data=raw_data,
            name=raw_data.get("name"),  # type: ignore[union-attr]
            description=raw_data.get("description"),  # type: ignore[union-attr]
            mime_type=mime_type,
            image=self.get_image_details(raw_data),  # type: ignore[arg-type]
            content=self.get_content_details(raw_data),  # type: ignore[arg-type]
            additional_fields=self.parse_additional_fields(raw_data),  # type: ignore[arg-type]  # noqa: E501
            attributes=[],
        )

    async def _gen_parse_metadata_impl(self, token: Token, raw_data: Optional[dict], *args, **kwargs) -> Optional[Metadata]:  # type: ignore[no-untyped-def, type-arg]  # noqa: E501
        mime_and_size, image, content = await asyncio.gather(
            self.fetcher.gen_fetch_mime_type_and_size(token.uri),  # type: ignore[arg-type]  # noqa: E501
            self.gen_image_details(raw_data),  # type: ignore[arg-type]  # noqa: E501
            self.gen_content_details(raw_data),  # type: ignore[arg-type]  # noqa: E501
        )
        mime_type, _ = mime_and_size

        return Metadata(
            token=token,
            raw_data=raw_data,
            name=raw_data.get("name"),  # type: ignore[union-attr]
            description=raw_data.get("description"),  # type: ignore[union-attr]
            mime_type=mime_type,
            image=image,  # type: ignore[arg-type]
            content=content,  # type: ignore[arg-type]
            additional_fields=self.parse_additional_fields(raw_data),  # type: ignore[arg-type]  # noqa: E501
            attributes=[],
        )
